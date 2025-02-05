import os.path
from typing import Any

def extract_keys_from_list(data):
    keys = []
    for item in data:
        if isinstance(item, dict):
            for key, value in item.items():
                keys.append(key)
                keys.extend(extract_keys_from_list([value]))
        elif isinstance(item, list):
            keys.extend(extract_keys_from_list(item))
    return list(set(keys))

def extract_values_from_list(data):
    values = []
    for item in data:
        if isinstance(item, dict):
            for value in item.values():
                if isinstance(value, (list, dict)):
                    values.extend(extract_values_from_list([value]) if isinstance(value, dict) else extract_values_from_list(value))
                else:
                    values.append(value)
        elif isinstance(item, list):
            values.extend(extract_values_from_list(item))
    return values

def save_data(data: Any, label: int, file_path=""):
    if isinstance(data, str):
        data = data.replace(",", " ")
    else:
        data = str(data).replace(",", " ")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n{data},{label}")

def create_file_if_not_exists(file_path):
    if os.path.isfile(file_path):
        return
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("text,")
        f.write("label")
