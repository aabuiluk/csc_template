# API-токени та ключі

**Ніколи не комітьте токени в git.** Лише змінні середовища.

## Де зберігати

| Де працюєте | Куди писати |
|-------------|-------------|
| Локально | `students/.env` (зразок: [students/.env.example](../students/.env.example)) |
| PythonAnywhere, сайт | **Web** → ваш додаток → **Environment variables** |
| PythonAnywhere, бот | **Tasks** → **Always-on** → **Environment variables** (ті самі ключі; див. [TELEGRAM_PA.md](TELEGRAM_PA.md)) |

Після зміни змінних на PA натисніть **Reload** (сайт) або перезапустіть Always-on.

## Як використовувати в `students/`

```python
from config import get_token, require_token

def register(app):
    @app.route("/weather")
    def weather():
        key = require_token("WEATHER_API_KEY")  # помилка, якщо не задано
        # ... запит до API з key ...

    @app.route("/rates")
    def rates():
        key = get_token("EXCHANGE_RATE_API_KEY")  # "" якщо немає
        if not key:
            return "Додайте EXCHANGE_RATE_API_KEY", 503
        ...
```

Довільні імена: `MY_BANK_API_KEY`, `NEWS_API_TOKEN` — головне, щоб збігалося в `.env` / на PA.

## Що не робити

- не кладіть ключі в `.py` файли в `students/`
- не пушіть `students/.env`
- не додавайте токени в README або коментарі

## Деплой

`git push` оновлює **код**, не токени. Токени лишаються в налаштуваннях PythonAnywhere.
