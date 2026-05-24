from flask import Blueprint, jsonify, render_template_string

from app.students import loaded_files

main_bp = Blueprint("main", __name__)

_HOME = """
<!doctype html>
<html lang="uk">
<head><meta charset="utf-8"><title>CSC</title></head>
<body>
  <h1>Проєкт на PythonAnywhere</h1>
  <p>Покладіть <code>.py</code> файли в <code>students/</code> — вони підхопляться після push.</p>
  <p>Завантажено: {{ files or '—' }}</p>
</body>
</html>
"""


@main_bp.route("/")
def index():
    files = ", ".join(loaded_files()) if loaded_files() else None
    return render_template_string(_HOME, files=files)


@main_bp.route("/health")
def health():
    return jsonify({"ok": True, "students": loaded_files()})
