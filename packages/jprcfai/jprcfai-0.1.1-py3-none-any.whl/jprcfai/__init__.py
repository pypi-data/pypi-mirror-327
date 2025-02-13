# jprcf/__init__.py

# Optional: automatically set the assistants directory so that unroll_prompt_from_file works.
import os
from importlib.resources import files


def resource_filename(package, resource):
    return str(files(package).joinpath(resource))


# Set the ASSISTANTS_DIR environment variable to point to the package's assistants folder.
assistants_dir = resource_filename(__name__, "assistants")
os.environ.setdefault("ASSISTANTS_DIR", assistants_dir)

# Import functions from core.py to expose them at the package level.
from .core import (
    ask_openai,
    unroll_prompt_from_file,
    get_repo_name,
    unroll_prompt_from_git,
    unroll_prompt,
    fix_single_code_file,
    execute_local_script_with_browser,
    ERROR_AFTER_TIMER,
    OK_AFTER_TIMER,
    WAIT_UNTIL_FINISH,
)
