import os
from pathlib import Path
from dotenv import load_dotenv
from utils_hj3415 import setup_logger

mylogger = setup_logger(__name__, "DEBUG")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

mylogger.debug(f"ENV_PATH: {ENV_PATH}")

# .env 로드 (없어도 에러 X)
load_dotenv(dotenv_path=ENV_PATH, override=True)

def get_env_variable(key: str, default=None):
    return os.getenv(key, default)


# 환경변수 로드 (없을 경우 기본값 할당)
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKENS = os.getenv("TELEGRAM_BOT_TOKENS")

mylogger.debug(f"GMAIL_USER={GMAIL_USER}")
mylogger.debug(f"GMAIL_APP_PASS={GMAIL_APP_PASS}")
mylogger.debug(f"TELEGRAM_CHAT_ID={TELEGRAM_CHAT_ID}")
mylogger.debug(f"TELEGRAM_BOT_TOKENS={TELEGRAM_BOT_TOKENS}")