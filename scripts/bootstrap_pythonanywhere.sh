#!/usr/bin/env bash
# Одноразове налаштування на PythonAnywhere (Bash console).
# Краще: python tools/pa_setup_gui.py на ПК → вставити згенерований блок сюди.

set -euo pipefail

GITHUB_REPO="${GITHUB_REPO:-https://github.com/YOUR_USER/csc_template.git}"
PROJECT_DIR="${PROJECT_DIR:-$HOME/csc_template}"
VENV_DIR="${VENV_DIR:-$HOME/.virtualenvs/csc-venv}"

echo "==> Clone"
if [[ ! -d "$PROJECT_DIR/.git" ]]; then
  git clone "$GITHUB_REPO" "$PROJECT_DIR"
else
  echo "Already cloned: $PROJECT_DIR"
  cd "$PROJECT_DIR" && git pull
fi

cd "$PROJECT_DIR"
git config merge.ours.driver true

echo "==> Virtualenv (python3.10 -m venv; mkvirtualenv часто недоступний)"
mkdir -p ~/.virtualenvs
if [[ ! -d "$VENV_DIR" ]]; then
  python3.10 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> post-merge hook"
HOOK="$PROJECT_DIR/.git/hooks/post-merge"
cat > "$HOOK" <<HOOK_EOF
#!/bin/sh
touch "\${PA_WSGI_FILE:-/var/www/__REPLACE_USERNAME___pythonanywhere_com_wsgi.py}" 2>/dev/null || true
HOOK_EOF
chmod +x "$HOOK"

echo ""
echo "Далі (Web tab — заповніть УСІ поля, потім Reload):"
echo "  Source code:      $PROJECT_DIR"
echo "  Working directory: $PROJECT_DIR"
echo "  Virtualenv:       $VENV_DIR"
echo "  WSGI: import sys; sys.path.insert(0, '$PROJECT_DIR'); from wsgi import application"
echo ""
echo "GitHub webhook: https://YOURUSER.pythonanywhere.com/deploy-webhook"
echo "Telegram: docs/TELEGRAM_PA.md (без allowlist в Account — його немає)"
echo "GUI майстер: python tools/pa_setup_gui.py"
echo ""
