import json
from pathlib import Path

DB_FILE = Path("data/applications.json")


def load_applications():
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text(encoding="utf-8"))


def save_application(entry):
    data = load_applications()
    data.append(entry)
    DB_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")