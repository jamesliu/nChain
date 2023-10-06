import os
from pathlib import Path

def user_dir():
    chain_user_path = os.environ.get("NANOCHAIN_USER_PATH")
    if chain_user_path:
        path = Path(chain_user_path)
    else:
        path = Path(os.path.expanduser("~/.nchain"))
    path.mkdir(exist_ok=True, parents=True)
    return path
