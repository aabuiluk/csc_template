# csc_template

Fork → додайте `.py` у **`students/`** → push → оновлення на [PythonAnywhere](https://www.pythonanywhere.com).

## Як працює `students/`

| Що в файлі | Коли виконується |
|------------|------------------|
| Код на верхньому рівні | При reload сайту (імпорт файлу) |
| `def register(app):` | Підключення маршрутів Flask |
| `def main():` | Always-on: `python run_students.py` |

Файли з іменем `_*.py` **не** запускаються (приклад: `_example_web.py`).

Підпапки підтримуються: `students/lab1/app.py` теж підхопиться.

**API-ключі** (погода, валюти, OpenAI, …): [docs/TOKENS.md](docs/TOKENS.md) — `from config import get_token`.

## Старт

1. [SETUP.md](SETUP.md) — PythonAnywhere + webhook  
2. Локально: `pip install -r requirements.txt` → `python run_local.py`

## Оновлення шаблону курсу

[docs/SYNC_TEMPLATE.md](docs/SYNC_TEMPLATE.md) — папка `students/` не перезапишеться.
