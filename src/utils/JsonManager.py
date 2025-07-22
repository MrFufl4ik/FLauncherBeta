import json
import os


def readJson(file_path: str) -> dict | None:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try: return json.load(f)
            except: pass
    return None


def writeJson(file_path: str, json_data: dict):
    existing_config: dict = {}
    if (readJson(file_path)): existing_config = readJson(file_path)
    existing_config.update(json_data)
    with open(file_path, 'w') as f:
        try:
            json.dump(existing_config, f, indent=4)
            return 0
        except: pass
    return 1
