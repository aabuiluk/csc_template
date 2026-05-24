# Файли з _ на початку не запускаються. Скопіюйте як my_site.py

from config import get_token


def register(app):
    @app.route("/hello")
    def hello():
        return "Привіт!"

    @app.route("/tokens-check")
    def tokens_check():
        """Перевірка, чи задані ключі (без показу значень)."""
        keys = ("WEATHER_API_KEY", "EXCHANGE_RATE_API_KEY", "OPENAI_API_KEY")
        status = {name: bool(get_token(name)) for name in keys}
        return status
