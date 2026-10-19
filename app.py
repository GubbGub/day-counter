"""
Day Counter Plan — a native macOS window for the PIC16F73 day counter build checklist.

The task list lives in ui/tasks.json (part of the repo, so anyone following along
sees the same plan). Your checkmarks live in a separate progress file on your Mac:

    ~/Library/Application Support/DayCounterPlan/progress.json

Keeping them apart means you can edit or add tasks in the repo without losing
progress, and your personal checkmarks never get committed by accident.
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import webview

APP_NAME = "Day Counter Plan"
DATA_DIR = Path.home() / "Library" / "Application Support" / "DayCounterPlan"
PROGRESS_FILE = DATA_DIR / "progress.json"


def resource_path(relative: str) -> Path:
    """Find bundled files both when run as a script and inside the PyInstaller .app."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative


TASKS_FILE = resource_path("ui/tasks.json")
INDEX_FILE = resource_path("ui/index.html")


def read_json(path: Path, fallback):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def write_json_atomic(path: Path, data) -> None:
    """Write to a temp file, then swap it in, so a crash mid-save can't corrupt progress."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


class Api:
    """Methods here are callable from JavaScript as window.pywebview.api.<name>()."""

    def load_state(self):
        tasks = read_json(TASKS_FILE, {"phases": []})
        progress = read_json(PROGRESS_FILE, {"done": {}, "updated": ""})
        valid_ids = {t["id"] for p in tasks["phases"] for t in p["tasks"]}
        done = {k: bool(v) for k, v in progress.get(
            "done", {}).items() if k in valid_ids}
        return {
            "phases": tasks["phases"],
            "done": done,
            "updated": progress.get("updated", ""),
        }

    def save_progress(self, done):
        updated = datetime.now().strftime("%b %d, %Y at %I:%M %p").replace(" 0", " ")
        clean = {str(k): True for k, v in dict(done).items() if v}
        write_json_atomic(PROGRESS_FILE, {"done": clean, "updated": updated})
        return {"updated": updated}


def main():
    webview.create_window(
        APP_NAME,
        url=INDEX_FILE.as_uri(),
        js_api=Api(),
        width=840,
        height=940,
        min_size=(420, 520),
    )
    webview.start()


if __name__ == "__main__":
    main()
