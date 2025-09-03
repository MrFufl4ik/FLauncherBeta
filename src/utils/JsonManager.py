import json
import os


def read_json(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f: return json.load(f)
    return {}


def write_json(file_path: str, json_data: dict) -> None:
    existing_config: dict = {}
    if read_json(file_path): existing_config = read_json(file_path)
    existing_config.update(json_data)
    with open(file_path, 'w') as f: json.dump(existing_config, f, indent=4)