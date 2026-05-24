# PythonAnywhere — швидке налаштування

## 1. Fork і clone на PA

```bash
git clone https://github.com/ВАШ_ЛОГІН/csc_template.git ~/csc_template
cd ~/csc_template
git config merge.ours.driver true
mkvirtualenv --python=python3.10 csc-venv
pip install -r requirements.txt
```

## 2. Web app

- **Manual configuration**, Python 3.10  
- Source: `/home/ВАШ_ЛОГІН/csc_template`  
- Virtualenv: `/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv`  
- WSGI:

```python
import sys
sys.path.insert(0, "/home/ВАШ_ЛОГІН/csc_template")
from wsgi import application
```

## 3. Змінні (Web → Environment variables)

З [.env.example](.env.example): `REPO_PATH`, `GITHUB_WEBHOOK_SECRET`, `PA_WSGI_FILE`.

## 4. GitHub webhook

- URL: `https://ВАШ_ЛОГІН.pythonanywhere.com/deploy-webhook`  
- Secret = `GITHUB_WEBHOOK_SECRET`  
- Подія: push  

## 5. Ваш код

Додайте файли в `students/`, наприклад `students/app.py`:

```python
def register(app):
    @app.route("/me")
    def me():
        return "Мій проєкт"
```

`git push` → сайт перезавантажиться з новим кодом.

## Telegram / фонові задачі

Always-on (платний план): команда

```bash
/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv/bin/python /home/ВАШ_ЛОГІН/csc_template/run_students.py
```

У `students/bot.py` — функція `main()` з `python-telegram-bot` (додайте в свій `requirements.txt` у форку).

Після deploy можна перезапускати задачу через `PA_ALWAYS_ON_TASK_ID` + API token.
