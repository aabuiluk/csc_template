"""Налаштування та доступ до токенів (змінні середовища, без commit у git)."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# 1) інфраструктура (деплой)  2) токени студента (локально students/.env, на PA — Web → Env)
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "students" / ".env")

REPO_PATH = Path(os.getenv("REPO_PATH", str(BASE_DIR)))

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

PA_WSGI_FILE = os.getenv("PA_WSGI_FILE", "")
PA_USERNAME = os.getenv("PA_USERNAME", "")
PA_API_TOKEN = os.getenv("PA_API_TOKEN", "")
PA_API_HOST = os.getenv("PA_API_HOST", "www.pythonanywhere.com")
PA_DOMAIN = os.getenv("PA_DOMAIN", "")
PA_ALWAYS_ON_TASK_ID = os.getenv("PA_ALWAYS_ON_TASK_ID", "")


def get_token(name: str, default: str = "") -> str:
    """Токен API з os.environ (PA dashboard, .env або students/.env)."""
    return os.getenv(name, default).strip()


def require_token(name: str) -> str:
    """Як get_token, але помилка якщо порожньо."""
    value = get_token(name)
    if not value:
        raise RuntimeError(
            f"Не задано змінну {name}. "
            f"Див. students/.env.example та docs/TOKENS.md"
        )
    return value
