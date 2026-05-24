#!/usr/bin/env python3
"""
Майстер налаштування PythonAnywhere — згенерувати команди для Bash-консолі PA.

Запуск (на своєму ПК): python tools/pa_setup_gui.py
Потрібен лише Python з tkinter (стандартна бібліотека).
"""

from __future__ import annotations

import secrets
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk


def _gen_secret() -> str:
    return secrets.token_hex(24)


class SetupWizard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CSC — налаштування PythonAnywhere")
        self.geometry("720x640")
        self.minsize(600, 500)

        outer = ttk.Frame(self, padding=10)
        outer.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        form = ttk.Frame(canvas)
        form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._fields: dict[str, tk.StringVar] = {}
        self._add_section(form, "Обліковий запис")
        self._add_field(form, "pa_username", "Логін PythonAnywhere", "mylogin")
        self._add_field(
            form,
            "pa_host",
            "Хост API (www або eu)",
            "www.pythonanywhere.com",
        )

        self._add_section(form, "Репозиторій GitHub")
        self._add_field(
            form,
            "github_repo",
            "URL форку (git clone)",
            "https://github.com/mylogin/csc_template.git",
        )
        self._add_field(form, "project_name", "Папка на PA", "csc_template")

        self._add_section(form, "Деплой")
        secret_var = self._add_field(
            form,
            "webhook_secret",
            "GITHUB_WEBHOOK_SECRET",
            "",
        )
        ttk.Button(
            form,
            text="Згенерувати секрет",
            command=lambda: secret_var.set(_gen_secret()),
        ).grid(row=form.grid_size()[1] - 1, column=2, sticky=tk.W, pady=2)

        self._add_field(
            form,
            "pa_api_token",
            "PA API token (опційно, для reload)",
            "",
        )
        self._add_field(
            form,
            "always_on_id",
            "PA_ALWAYS_ON_TASK_ID (опційно)",
            "",
        )

        self._add_section(form, "API-ключі студента (опційно)")
        for key, label in (
            ("TELEGRAM_BOT_TOKEN", "Telegram bot token"),
            ("WEATHER_API_KEY", "Погода"),
            ("EXCHANGE_RATE_API_KEY", "Курси валют"),
            ("OPENAI_API_KEY", "OpenAI"),
        ):
            self._add_field(form, key, label, "")

        self._add_section(form, "Опції")
        self._use_bot = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form,
            text="Є Telegram-бот (Always-on, платний план)",
            variable=self._use_bot,
        ).grid(column=0, columnspan=3, sticky=tk.W, pady=4)

        btns = ttk.Frame(self, padding=(10, 0))
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Згенерувати", command=self._generate).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btns, text="Копіювати все", command=self._copy_all).pack(
            side=tk.LEFT, padx=4
        )

        self._output = scrolledtext.ScrolledText(
            self, height=18, font=("Menlo", 11), wrap=tk.WORD
        )
        self._output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(
            self,
            text="Вставте блок «1. Bash» у консоль PythonAnywhere. Решту — у Web / GitHub вручну.",
            wraplength=680,
        ).pack(padx=10, pady=(0, 8))

    def _add_section(self, parent: ttk.Frame, title: str) -> None:
        ttk.Label(parent, text=title, font=("", 11, "bold")).grid(
            column=0, columnspan=3, sticky=tk.W, pady=(12, 4)
        )

    def _add_field(
        self, parent: ttk.Frame, key: str, label: str, default: str
    ) -> tk.StringVar:
        row = parent.grid_size()[1]
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        var = tk.StringVar(value=default)
        ttk.Entry(parent, textvariable=var, width=52).grid(
            row=row, column=1, columnspan=2, sticky=tk.EW, pady=2
        )
        parent.columnconfigure(1, weight=1)
        self._fields[key] = var
        return var

    def _values(self) -> dict[str, str]:
        return {k: v.get().strip() for k, v in self._fields.items()}

    def _generate(self) -> None:
        v = self._values()
        user = v["pa_username"]
        if not user:
            messagebox.showerror("Помилка", "Вкажіть логін PythonAnywhere")
            return

        host = v["pa_host"] or "www.pythonanywhere.com"
        domain = f"{user}.pythonanywhere.com"
        project = v["project_name"] or "csc_template"
        home = f"/home/{user}"
        project_dir = f"{home}/{project}"
        venv = f"{home}/.virtualenvs/csc-venv"
        wsgi_file = f"/var/www/{user}_pythonanywhere_com_wsgi.py"
        repo = v["github_repo"] or f"https://github.com/{user}/{project}.git"
        secret = v["webhook_secret"] or _gen_secret()

        bash = f"""# === 1. Bash — вставте в консоль PythonAnywhere ===
git clone {repo} {project_dir} || (cd {project_dir} && git pull)
cd {project_dir}
git config merge.ours.driver true

mkdir -p ~/.virtualenvs
python3.10 -m venv ~/.virtualenvs/csc-venv
source ~/.virtualenvs/csc-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Далі: Web tab (див. блок 2 нижче) і GitHub webhook (блок 3)"
"""

        web_env = [f"REPO_PATH={project_dir}", f"GITHUB_WEBHOOK_SECRET={secret}"]
        web_env.append(f"PA_WSGI_FILE={wsgi_file}")
        web_env.append(f"PA_USERNAME={user}")
        web_env.append(f"PA_DOMAIN={domain}")
        web_env.append(f"PA_API_HOST={host}")
        if v["pa_api_token"]:
            web_env.append(f"PA_API_TOKEN={v['pa_api_token']}")
        if v["always_on_id"]:
            web_env.append(f"PA_ALWAYS_ON_TASK_ID={v['always_on_id']}")
        for key in (
            "TELEGRAM_BOT_TOKEN",
            "WEATHER_API_KEY",
            "EXCHANGE_RATE_API_KEY",
            "OPENAI_API_KEY",
        ):
            if v.get(key):
                web_env.append(f"{key}={v[key]}")

        web_block = (
            "# === 2. Web → ваш сайт → Environment variables (кожен рядок KEY=VALUE) ===\n"
            + "\n".join(web_env)
            + "\n\n# === 2b. Web → Code (заповніть поля, потім зелена кнопка Reload) ===\n"
            + f"Source code:     {project_dir}\n"
            + f"Working directory: {project_dir}\n"
            + f"Virtualenv:      {venv}\n"
            + f"WSGI file:       {wsgi_file}\n"
            + "\n# Вміст WSGI file:\n"
            + f"import sys\nsys.path.insert(0, '{project_dir}')\nfrom wsgi import application\n"
        )

        webhook = f"""# === 3. GitHub → Settings → Webhooks → Add webhook ===
Payload URL:   https://{domain}/deploy-webhook
Content type:  application/json
Secret:        {secret}
Events:        Just the push event
"""

        always_on = ""
        if self._use_bot.get():
            always_on = f"""
# === 4. Tasks → Always-on (платний план) ===
Command:
{venv}/bin/python {project_dir}/run_students.py

Environment: TELEGRAM_BOT_TOKEN=... (як у Web)
Див. docs/TELEGRAM_PA.md — без trust_env=False, api.telegram.org уже в whitelist PA.
"""

        checklist = """
# === Чекліст (не робіть «allowlist» в Account — такого розділу немає) ===
[ ] Web: Manual configuration, Python 3.10
[ ] Усі поля Code заповнені (не лишайте порожніми)
[ ] Reload після змін
[ ] curl https://""" + domain + "/health\n"

        text = "\n".join(
            [bash, web_block, webhook, always_on, checklist]
        ).strip() + "\n"
        self._output.delete("1.0", tk.END)
        self._output.insert(tk.END, text)

    def _copy_all(self) -> None:
        text = self._output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Підказка", "Спочатку натисніть «Згенерувати»")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Готово", "Скопійовано в буфер обміну")


def main() -> None:
    app = SetupWizard()
    app.mainloop()


if __name__ == "__main__":
    main()
