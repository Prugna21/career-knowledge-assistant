import json
from pathlib import Path
from datetime import datetime
import uuid

DB_FILE = Path(__file__).resolve().parent / "data" / "jobs" / "applications.json"


def load_applications():
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text(encoding="utf-8"))


def save_all(data):
    DB_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def save_application(entry):
    data = load_applications()

    entry["id"] = str(uuid.uuid4())
    entry["created_at"] = str(datetime.now())
    entry["status"] = entry.get("status", "saved")

    data.append(entry)

    save_all(data)


def delete_application(app_id):
    data = load_applications()

    new_data = [a for a in data if a.get("id") != app_id]

    save_all(new_data)


def update_application(app_id, updates: dict):
    data = load_applications()

    for app in data:
        if app.get("id") == app_id:
            app.update(updates)

    save_all(data)