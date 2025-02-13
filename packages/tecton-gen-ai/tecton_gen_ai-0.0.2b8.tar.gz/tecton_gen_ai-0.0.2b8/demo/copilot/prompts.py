import datetime
import json
import os

from constants import FILE_DIR
from utils import get_cwd, is_in_feature_repo

# Ultra hacky - i'm setting this in lib.py's init_copilot because there's a race condition
TECTON_ACCOUNT_INFO = None


def sys_prompt() -> str:
    context = {
        "Current directory": get_cwd(),
        "In feature repo": is_in_feature_repo(),
        "Current Tecton account info": TECTON_ACCOUNT_INFO,
        "Current time": datetime.datetime.now().isoformat(),
    }
    with open(os.path.join(FILE_DIR, "data", "gotchas.md"), "r") as f:
        gotchas = f.read()
    with open(os.path.join(FILE_DIR, "data", "sys_prompt.md"), "r") as f:
        return f.read().format(context=json.dumps(context, indent=4), gotchas=gotchas)
