# Скопіюйте як students/bot.py (без _ — файл запуститься через run_students.py)
# На PythonAnywhere free tier: requests має використовувати проксі PA (НЕ trust_env=False).

from __future__ import annotations

import logging
import time

import requests

from config import require_token

logger = logging.getLogger(__name__)
_API = "https://api.telegram.org/bot{token}/{method}"


def _api(session: requests.Session, token: str, method: str, **params):
    url = _API.format(token=token, method=method)
    delay = 1.0
    for attempt in range(6):
        try:
            resp = session.get(url, params=params, timeout=35)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok"):
                raise RuntimeError(data)
            return data
        except Exception:
            if attempt >= 5:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 60.0)


def _send(session: requests.Session, token: str, chat_id: int, text: str) -> None:
    _api(session, token, "sendMessage", chat_id=chat_id, text=text)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    token = require_token("TELEGRAM_BOT_TOKEN")
    session = requests.Session()

    offset = 0
    try:
        pending = _api(session, token, "getUpdates", timeout=1).get("result") or []
        if pending:
            offset = pending[-1]["update_id"] + 1
            logger.info("Skipped %s old updates", len(pending))
    except Exception:
        logger.exception("Could not skip old updates")

    logger.info("Bot polling started")
    while True:
        try:
            data = _api(
                session,
                token,
                "getUpdates",
                timeout=30,
                offset=offset,
            )
            for update in data.get("result") or []:
                offset = update["update_id"] + 1
                message = update.get("message") or {}
                text = (message.get("text") or "").strip().lower()
                chat_id = message.get("chat", {}).get("id")
                if not chat_id:
                    continue
                if text in ("/start", "start", "hi", "hello", "привіт"):
                    _send(session, token, chat_id, "Привіт! Бот на PythonAnywhere працює.")
        except Exception:
            logger.exception("Polling error")
            time.sleep(5)
