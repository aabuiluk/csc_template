# csc_template

Fork → `.py` у **`students/`** → push → [PythonAnywhere](https://www.pythonanywhere.com).

## Старт

| Крок | Дія |
|------|-----|
| 1 | **Fork** на GitHub |
| 2 | **`python tools/pa_setup_gui.py`** — згенерувати команди для консолі PA |
| 3 | [SETUP.md](SETUP.md) — Web, webhook, токени |
| 4 | Код у `students/` |

## `students/`

| У файлі | Ефект |
|---------|--------|
| Код на верхньому рівні | Імпорт при reload сайту |
| `def register(app):` | Маршрути Flask |
| `def main():` | Always-on: `run_students.py` |
| `_*.py` | Не запускаються (приклади) |

**Токени:** [docs/TOKENS.md](docs/TOKENS.md) · **Telegram на PA:** [docs/TELEGRAM_PA.md](docs/TELEGRAM_PA.md)

## Оновлення шаблону курсу

[docs/SYNC_TEMPLATE.md](docs/SYNC_TEMPLATE.md)
