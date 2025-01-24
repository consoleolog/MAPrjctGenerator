import getpass
import os
from dotenv import load_dotenv

def set_env(var: str):
    load_dotenv()
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}")

