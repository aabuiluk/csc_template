"""Усі students/**/*.py (крім _*) підхоплюються при старті сервера."""

from __future__ import annotations

import importlib.util
import logging
import threading
from pathlib import Path

from flask import Flask

import config

logger = logging.getLogger(__name__)
_loaded: list[str] = []


def students_dir() -> Path:
    return config.REPO_PATH / "students"


def iter_student_files() -> list[Path]:
    root = students_dir()
    if not root.is_dir():
        return []
    files = [
        p
        for p in sorted(root.rglob("*.py"))
        if not p.name.startswith("_")
    ]
    return files


def _load(path: Path):
    rel = path.relative_to(students_dir())
    module_name = "students_" + rel.as_posix().replace("/", ".").removesuffix(".py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_for_web(app: Flask) -> None:
    """Імпорт кожного файлу; register(app) — якщо є."""
    _loaded.clear()
    for path in iter_student_files():
        module = _load(path)
        _loaded.append(str(path.relative_to(students_dir())))
        if hasattr(module, "register"):
            module.register(app)
        logger.info("students: loaded %s", path.name)


def loaded_files() -> list[str]:
    return list(_loaded)


def run_background() -> None:
    """Always-on на PA: python run_students.py — main() у кожному файлі в окремому потоці."""
    threads: list[threading.Thread] = []
    for path in iter_student_files():
        module = _load(path)
        rel = path.relative_to(students_dir())
        if hasattr(module, "main"):
            t = threading.Thread(
                target=module.main,
                name=f"students-{rel.stem}",
                daemon=True,
            )
            t.start()
            threads.append(t)
            logger.info("students: started main() in %s", rel)
        else:
            logger.info("students: imported %s (no main)", rel)

    if not threads:
        logger.warning("students/: немає файлів з функцією main()")
        threading.Event().wait()
        return

    threading.Event().wait()
