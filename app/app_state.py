import json
from pathlib import Path
from datetime import datetime
import uuid

DB_FILE = Path("data/applications.json")


def load_applications():
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text(encoding="utf-8"))


def save_application(entry):
    data = load_applications()

    entry["id"] = str(uuid.uuid4())
    entry["created_at"] = entry.get("created_at", str(datetime.now()))
    entry["status"] = entry.get("status", "saved")

    data.append(entry)

    DB_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def save_all(data):
    DB_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def delete_application(app_id):
    data = load_applications()
    data = [a for a in data if a.get("id") != app_id]
    save_all(data)


def update_application(app_id, updates: dict):
    data = load_applications()

    for app in data:
        if app.get("id") == app_id:
            app.update(updates)

    DB_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
def delete_application(app_id):
    data = load_applications()
    data = [a for a in data if a.get("id") != app_id]

    DB_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )