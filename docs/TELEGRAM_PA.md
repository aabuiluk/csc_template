# Telegram-бот на PythonAnywhere

## Allowlist — нічого додавати не треба

На безкоштовному плані **немає** розділу в Account/Web, куди студент сам додає `api.telegram.org`.

Дозволені хости веде PythonAnywhere: https://www.pythonanywhere.com/whitelist/ — `api.telegram.org` уже там.

## Проксі (обов’язково на free tier)

Зовнішні HTTP-запити з консолі та Always-on йдуть через проксі PA. Деталі:  
https://help.pythonanywhere.com/pages/403ForbiddenError/#proxy-details

| Помилка | Ймовірна причина |
|---------|------------------|
| `[Errno 101] Network is unreachable` | Код **обходить** проксі (`trust_env=False`, власний проксі) |
| `ProxyError 503` | Тимчасовий збій PA або неправильна сесія requests |
| Нескінченний JSON у консолі | `getUpdates` **без offset** — бот знову читає ту саму чергу |

**Рекомендація:** `requests.Session()` без `trust_env=False`, long polling `timeout=30`, параметр **`offset`**, retry з backoff.

Готовий приклад: скопіюйте [`students/_example_bot.py`](../students/_example_bot.py) → `students/bot.py`.

`python-telegram-bot` у шаблоні **немає** — додавайте у свій `requirements.txt` у форку, якщо потрібен саме він (і налаштуйте проксі за документацією PA).

## Always-on

1. **Tasks** → **Always-on tasks** → команда:

```bash
/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv/bin/python /home/ВАШ_ЛОГІН/csc_template/run_students.py
```

2. **Environment variables** у задачі: `TELEGRAM_BOT_TOKEN=...` (ті самі ключі, що для сайту).

3. Після `git push` — reload сайту; за бажанням `PA_ALWAYS_ON_TASK_ID` для перезапуску через API.

## Перевірка в Bash

```bash
source ~/.virtualenvs/csc-venv/bin/activate
cd ~/csc_template
export TELEGRAM_BOT_TOKEN='ваш_токен'
python -c "import requests; print(requests.get('https://api.telegram.org').status_code)"
```

Очікується `200` або `404`, не `Network is unreachable`.
