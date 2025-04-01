import os
from pathlib import Path
from dotenv import load_dotenv
from utils_hj3415 import setup_logger

mylogger = setup_logger(__name__, "INFO")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

mylogger.debug(f"ENV_PATH: {ENV_PATH}")

# .env 로드 (없어도 에러 X)
load_dotenv(dotenv_path=ENV_PATH, override=True)

def get_env_variable(key: str, default=None):
    return os.getenv(key, default)
