"""GitHub webhook → git pull → reload."""

from __future__ import annotations

import hashlib
import hmac
import logging
import subprocess
from pathlib import Path

import requests
from flask import Blueprint, abort, request

import config

logger = logging.getLogger(__name__)
deploy_bp = Blueprint("deploy", __name__)


def _verify_github_signature(payload: bytes, signature_header: str | None) -> bool:
    secret = config.GITHUB_WEBHOOK_SECRET
    if not secret:
        return False
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = (
        "sha256="
        + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    )
    return hmac.compare_digest(expected, signature_header)


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _git_pull() -> None:
    repo = config.REPO_PATH
    _run(["git", "fetch", "origin"], repo)
    for branch in ("main", "master"):
        try:
            _run(["git", "checkout", branch], repo)
            _run(["git", "pull", "origin", branch], repo)
            return
        except subprocess.CalledProcessError:
            continue
    raise subprocess.CalledProcessError(1, "git pull", "", "No main/master branch")


def _pip_install() -> None:
    req = config.REPO_PATH / "requirements.txt"
    if req.is_file():
        _run(["pip", "install", "-r", str(req)], config.REPO_PATH)


def _reload_webapp() -> None:
    if config.PA_WSGI_FILE:
        Path(config.PA_WSGI_FILE).touch()
        return
    if config.PA_USERNAME and config.PA_API_TOKEN and config.PA_DOMAIN:
        url = (
            f"https://{config.PA_API_HOST}/api/v0/user/"
            f"{config.PA_USERNAME}/webapps/{config.PA_DOMAIN}/reload/"
        )
        requests.post(
            url,
            headers={"Authorization": f"Token {config.PA_API_TOKEN}"},
            timeout=60,
        ).raise_for_status()


def _restart_always_on() -> None:
    if not config.PA_ALWAYS_ON_TASK_ID:
        return
    if not (config.PA_USERNAME and config.PA_API_TOKEN):
        return
    url = (
        f"https://{config.PA_API_HOST}/api/v0/user/"
        f"{config.PA_USERNAME}/always_on/{config.PA_ALWAYS_ON_TASK_ID}/restart/"
    )
    requests.post(
        url,
        headers={"Authorization": f"Token {config.PA_API_TOKEN}"},
        timeout=60,
    ).raise_for_status()


@deploy_bp.route("/deploy-webhook", methods=["POST"])
def deploy_webhook():
    if not _verify_github_signature(
        request.data, request.headers.get("X-Hub-Signature-256")
    ):
        abort(403)
    event = request.headers.get("X-GitHub-Event", "")
    if event == "ping":
        return "", 204
    if event != "push":
        return "ignored", 200
    try:
        _git_pull()
        _pip_install()
        _reload_webapp()
        _restart_always_on()
    except subprocess.CalledProcessError as exc:
        return (exc.stderr or str(exc)), 500
    return "deployed", 200
