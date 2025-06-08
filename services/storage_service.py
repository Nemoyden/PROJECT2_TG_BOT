import json
from pathlib import Path

STORAGE_PATH = Path("storage/habits.json")

def load_habits():
    if not STORAGE_PATH.exists():
        return {}
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_habits(data):
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
