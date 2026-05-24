"""Налаштування для PythonAnywhere."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

REPO_PATH = Path(os.getenv("REPO_PATH", str(BASE_DIR)))

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

PA_WSGI_FILE = os.getenv("PA_WSGI_FILE", "")
PA_USERNAME = os.getenv("PA_USERNAME", "")
PA_API_TOKEN = os.getenv("PA_API_TOKEN", "")
PA_API_HOST = os.getenv("PA_API_HOST", "www.pythonanywhere.com")
PA_DOMAIN = os.getenv("PA_DOMAIN", "")
PA_ALWAYS_ON_TASK_ID = os.getenv("PA_ALWAYS_ON_TASK_ID", "")
