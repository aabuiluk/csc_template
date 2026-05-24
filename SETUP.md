# PythonAnywhere — налаштування

## Швидко: GUI-майстер (рекомендовано)

На **своєму комп’ютері** (не на PA):

```bash
python tools/pa_setup_gui.py
```

Заповніть поля → **Згенерувати** → скопіюйте блок **«1. Bash»** у консоль PythonAnywhere. Блоки 2–3 — у Web tab і GitHub.

---

## 1. Fork і clone на PA

```bash
git clone https://github.com/ВАШ_ЛОГІН/csc_template.git ~/csc_template
cd ~/csc_template
git config merge.ours.driver true

mkdir -p ~/.virtualenvs
python3.10 -m venv ~/.virtualenvs/csc-venv
source ~/.virtualenvs/csc-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> `mkvirtualenv` на PA часто **не працює** — використовуйте `python3.10 -m venv`.

Або: `bash scripts/bootstrap_pythonanywhere.sh` (після `export GITHUB_REPO=...`).

---

## 2. Web app — усі поля обов’язкові

**Web** → **Add a new web app** → **Manual configuration** → Python **3.10**.

| Поле | Значення |
|------|----------|
| **Source code** | `/home/ВАШ_ЛОГІН/csc_template` |
| **Working directory** | `/home/ВАШ_ЛОГІН/csc_template` |
| **Virtualenv** | `/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv` (повний шлях) |

**WSGI configuration file** — замініть вміст:

```python
import sys
sys.path.insert(0, "/home/ВАШ_ЛОГІН/csc_template")
from wsgi import application
```

Натисніть зелену кнопку **Reload** після будь-яких змін.

Перевірка: https://ВАШ_ЛОГІН.pythonanywhere.com/health

---

## 3. Змінні середовища

**Web** → ваш сайт → **Environment variables**:

- Деплой: `REPO_PATH`, `GITHUB_WEBHOOK_SECRET`, `PA_WSGI_FILE`, `PA_USERNAME`, `PA_DOMAIN`
- Ваші API: `TELEGRAM_BOT_TOKEN`, `WEATHER_API_KEY`, … — [docs/TOKENS.md](docs/TOKENS.md)

`PA_WSGI_FILE` = `/var/www/вашлогін_pythonanywhere_com_wsgi.py` (шлях з Web → WSGI file).

**Reload** після зміни змінних.

---

## 4. GitHub webhook

| Поле | Значення |
|------|----------|
| Payload URL | `https://ВАШ_ЛОГІН.pythonanywhere.com/deploy-webhook` |
| Secret | = `GITHUB_WEBHOOK_SECRET` |
| Events | push |

---

## 5. Код у `students/`

```python
from config import get_token

def register(app):
    @app.route("/me")
    def me():
        return "Мій проєкт"
```

`git push` → сайт оновиться.

---

## Telegram-бот

- **Немає** «allowlist» в Account/Web — `api.telegram.org` уже в [глобальному списку PA](https://www.pythonanywhere.com/whitelist/).
- На free tier потрібен **проксі PA** для `requests` — див. [docs/TELEGRAM_PA.md](docs/TELEGRAM_PA.md).
- Приклад: `students/_example_bot.py` → скопіювати як `students/bot.py`.
- **Always-on** (платний план):

```bash
/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv/bin/python /home/ВАШ_ЛОГІН/csc_template/run_students.py
```

Токен `TELEGRAM_BOT_TOKEN` — також у **Environment** Always-on задачі.

`python-telegram-bot` у шаблоні **не входить** у `requirements.txt` — лише `requests` (як у прикладі).
