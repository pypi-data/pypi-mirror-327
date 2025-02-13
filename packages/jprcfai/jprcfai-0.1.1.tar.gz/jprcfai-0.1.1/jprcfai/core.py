import os
import re
import subprocess
import webbrowser
import tempfile
import time
import requests
from platformdirs import user_cache_dir


# Constants for execution modes
ERROR_AFTER_TIMER = (
    "ERROR_AFTER_TIMER"  # For servers: after wait_time, process must be running.
)
OK_AFTER_TIMER = "OK_AFTER_TIMER"  # For scripts: after wait_time, if no errors are detected, it is considered OK.
WAIT_UNTIL_FINISH = "WAIT_UNTIL_FINISH"  # Always wait until the process finishes.


def ask_openai(user_prompt, headers, reasoning_effort):
    """
    Sends the user_prompt to the OpenAI API and returns the answer.
    This function centralizes the API request logic to avoid duplication.
    """
    payload = {
        "model": "o3-mini",
        "reasoning_effort": reasoning_effort,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    print("Processing question...")
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as req_err:
        print(f"Request to OpenAI failed:\n{req_err}")
        return None

    response_json = response.json()
    if "choices" not in response_json or not response_json["choices"]:
        print("Error: Unexpected response from OpenAI:", response_json)
        return None

    return response_json["choices"][0]["message"]["content"]


def unroll_prompt_from_file(filename, dir=None):
    """
    Reads the file content from a directory specified by the
    ASSISTANTS_DIR environment variable.
    """
    base_dir = dir if dir else os.environ.get("ASSISTANTS_DIR", "")
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def get_repo_name(git_url):
    """
    Extracts the repository name from a git URL.
    For example, given "git@github.com:username/repo.git" or
    "https://github.com/username/repo.git" it returns "repo".
    """
    # Handle SSH-style URL (with colon)
    if "@" in git_url and ":" in git_url:
        part = git_url.split(":")[-1]  # e.g., "username/repo.git"
    else:
        # Handle HTTPS-style URL.
        part = git_url.rstrip("/").split("/")[-1]
    if part.endswith(".git"):
        part = part[:-4]
    return part


def unroll_prompt_from_git(git_url, file_location, branch):
    """
    Clones (or updates) a repository in a user-specific cache folder,
    then retrieves the content of a file from the specified branch.
    """
    repo_name = get_repo_name(git_url)

    # 1) Determine the user cache directory for your project:
    #    The second argument can be your organization or username, if desired.
    cache_dir = user_cache_dir("jprcfai")
    repos_dir = os.path.join(cache_dir, "repos")
    os.makedirs(repos_dir, exist_ok=True)

    # 2) Clone or update the repo inside the cache directory.
    repo_path = os.path.join(repos_dir, repo_name)
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", git_url, repo_path], check=True)
    else:
        subprocess.run(["git", "-C", repo_path, "fetch"], check=True)

    # 3) Use 'git show' to grab the file contents.
    result = subprocess.run(
        ["git", "-C", repo_path, "show", f"{branch}:{file_location}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def unroll_prompt(prompt, visited=None):
    """
    Recursively replaces placeholders in the prompt with their loaded content.

    There are two placeholder types:

    1. [#PLACEHOLDER_LOAD_FROM_FILE (<prompt_label>)]
       -> Loads content from a local file.

    2. [#PLACEHOLDER_LOAD_FILE_FROM_GIT (<git_url_ssh>, <file_location>, <branch>)]
       -> Clones or updates a git repository and loads content from a file in that repo.

    The visited set (of command tuples) prevents the same placeholder command
    from being processed more than once (avoiding infinite recursion).
    """
    if visited is None:
        visited = set()

    # Regular expression for file-based placeholders:
    file_pattern = re.compile(r"\[#PLACEHOLDER_LOAD_FROM_FILE\s*\(\s*([^)]+?)\s*\)\]")
    # Regular expression for git-based placeholders:
    git_pattern = re.compile(
        r"\[#PLACEHOLDER_LOAD_FILE_FROM_GIT\s*\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)\]"
    )

    def file_repl(match):
        filename = match.group(1).strip()
        key = ("LOAD_FROM_FILE", filename)
        if key in visited:
            # Already processed this file; avoid reprocessing.
            return match.group(0)
        visited.add(key)
        try:
            content = unroll_prompt_from_file(filename)
        except Exception as e:
            content = f"[Error loading file '{filename}': {e}]"
        # Process any placeholders within the loaded content recursively.
        return unroll_prompt(content, visited)

    def git_repl(match):
        git_url = match.group(1).strip()
        file_location = match.group(2).strip()
        branch = match.group(3).strip()
        key = ("LOAD_FROM_GIT", git_url, file_location, branch)
        if key in visited:
            return match.group(0)
        visited.add(key)
        try:
            content = unroll_prompt_from_git(git_url, file_location, branch)
        except Exception as e:
            content = (
                f"[Error loading from git ({git_url}, {file_location}, {branch}): {e}]"
            )
        # Recursively process the loaded content.
        return unroll_prompt(content, visited)

    # First, replace any file-based placeholders.
    prompt = file_pattern.sub(file_repl, prompt)
    # Then, replace any git-based placeholders.
    prompt = git_pattern.sub(git_repl, prompt)

    return prompt


def fix_single_code_file(
    answer, headers, execution_command, reasoning_effort, wait_time, mode
):
    """
    Iteratively writes the provided code (answer) to a temporary file, launches it using the specified
    execution_command, checks for startup errors according to the specified wait_time and mode, and,
    if errors are detected, attempts to fix them by sending an update request to OpenAI.
    The temporary file is deleted after execution.

    Parameters:
      answer: The code to execute.
      headers: Headers for OpenAI API calls.
      execution_command: Command to execute the code (e.g., "node").
      reasoning_effort: The reasoning effort for execution (error fixes use 'medium').
      wait_time: Time in seconds to wait after process launch to check status. If None, waits until the process finishes.
      mode: One of the following modes:
            ERROR_AFTER_TIMER: For servers. After wait_time seconds, the process must be running.
            OK_AFTER_TIMER: For scripts. After wait_time seconds, if no errors are found, it is considered OK.
            WAIT_UNTIL_FINISH: Waits for the process to finish, then checks the exit code.
    Returns:
      The final code (answer) that was executed successfully.
    """
    while True:
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".js", encoding="utf-8"
            ) as tmp_file:
                tmp_file.write(answer)
                tmp_filepath = tmp_file.name
        except Exception as exc:
            print("Failed to write to temporary file:", exc)
            return None

        print(f"Launching with '{execution_command} {tmp_filepath}' ...")

        process = subprocess.Popen(
            [execution_command, tmp_filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        success = False

        if wait_time is not None and mode != WAIT_UNTIL_FINISH:
            time.sleep(wait_time)
            ret = process.poll()

            if mode == ERROR_AFTER_TIMER:
                if ret is not None:
                    outs, errs = process.communicate()
                    error_message = (
                        errs.strip()
                        if errs.strip()
                        else f"{execution_command} exited with code {ret}"
                    )
                    print(
                        f"\nError detected: Process terminated in ERROR_AFTER_TIMER mode:\n{error_message}"
                    )
                else:
                    success = True
                    process.terminate()
                    process.wait()

            elif mode == OK_AFTER_TIMER:
                if ret is None:
                    success = True
                    process.terminate()
                    process.wait()
                else:
                    retcode = process.returncode
                    if retcode == 0:
                        success = True
                    else:
                        outs, errs = process.communicate()
                        error_message = (
                            errs.strip()
                            if errs.strip()
                            else f"{execution_command} exited with code {retcode}"
                        )
                        print(
                            f"\nError detected in OK_AFTER_TIMER mode:\n{error_message}"
                        )

        else:
            retcode = process.wait()
            if retcode == 0:
                success = True
            else:
                outs, errs = process.communicate()
                error_message = (
                    errs.strip()
                    if errs.strip()
                    else f"{execution_command} exited with code {retcode}"
                )
                print(f"\nError detected in WAIT_UNTIL_FINISH mode:\n{error_message}")

        try:
            os.unlink(tmp_filepath)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {tmp_filepath}: {e}")

        if success:
            print(f"\n{execution_command} executed successfully under mode {mode}.")
            break
        else:
            print(
                "\nAttempting to fix the error by updating the code with reasoning set to 'medium'..."
            )
            fix_file_content = unroll_prompt_from_file("CodeFixer.txt")
            fix_file_content = unroll_prompt(fix_file_content)
            new_user_prompt = fix_file_content.replace("[FILE_CODE]", answer)
            new_user_prompt = new_user_prompt.replace("[ERROR]", error_message)
            new_answer = ask_openai(new_user_prompt, headers, reasoning_effort)
            if new_answer is None:
                print("Failed to receive a fixed code from OpenAI. Exiting.")
                return None
            answer = new_answer
            print("Updated code received. Retrying execution...\n")

    return answer


def execute_local_script_with_browser(code, execution_command, port):
    """
    Executes the provided code by writing it to a temporary file and launching it
    using the given command. Immediately launches the default web browser to the specified port.

    Parameters:
      code: The code to execute.
      execution_command: Command to execute the code (e.g., "node").
      port: Port number for launching the browser.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".js", encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(code)
            tmp_filepath = tmp_file.name
    except Exception as exc:
        print("Failed to write to temporary file:", exc)
        return None

    print("\nExecuting final code from temporary file:", tmp_filepath)
    process = subprocess.Popen(
        [execution_command, tmp_filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    webbrowser.open(f"http://localhost:{port}")
    print(f"\nBrowser launched to http://localhost:{port}.")

    process.wait()

    try:
        os.unlink(tmp_filepath)
    except Exception as e:
        print(f"Warning: Could not delete temporary file {tmp_filepath}: {e}")
