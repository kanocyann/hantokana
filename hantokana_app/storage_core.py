import json
import os
import sys
from pathlib import Path

from .conversion_core import empty_custom_dict, ensure_custom_dict_schema
from .app_config import merge_app_config, normalize_app_config


APP_NAME = "Hantokana"
_MISSING = object()


def get_appdata_path(app_name=APP_NAME):
    appdata = os.getenv("APPDATA")
    if not appdata:
        appdata = os.path.join(str(Path.home()), "AppData", "Roaming")
    app_dir = os.path.join(appdata, app_name)
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def get_dict_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "custom_dict.json")


def get_official_dict_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "official_dict.json")


def get_effective_dict_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "effective_dict.json")


def get_config_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "config.json")


def resource_path(relative_path, base_file=None):
    base_path = getattr(sys, "_MEIPASS", None)
    if not base_path:
        try:
            reference = base_file or __file__
            base_path = os.path.dirname(os.path.abspath(reference))
        except Exception:
            base_path = os.path.dirname(os.path.abspath("."))

    candidate = os.path.join(base_path, relative_path)
    if os.path.exists(candidate):
        return candidate

    project_root = os.path.dirname(base_path)
    root_candidate = os.path.join(project_root, relative_path)
    if os.path.exists(root_candidate):
        return root_candidate

    return candidate


def _ensure_parent_dir(path):
    parent_dir = os.path.dirname(path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)


def load_json_file(path, default=_MISSING):
    if default is _MISSING:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return default


def save_json_file(path, data, indent=4):
    _ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def load_config(config_path):
    config = load_json_file(config_path, default={})
    normalized = normalize_app_config(config)
    if normalized != config:
        save_json_file(config_path, normalized, indent=4)
    return normalized


def save_config(config_path, config):
    existing = load_json_file(config_path, default={})
    merged = merge_app_config(existing, config if isinstance(config, dict) else {})
    save_json_file(config_path, merged, indent=4)


def load_custom_dict(dict_path, initial_resource_path=None):
    if not os.path.exists(dict_path):
        save_json_file(dict_path, empty_custom_dict(), indent=2)

    custom_dict = ensure_custom_dict_schema(load_json_file(dict_path, default=empty_custom_dict()))
    return custom_dict, dict_path


def sync_official_dict_to_appdata(source_path, target_path):
    official_dict = load_official_dict(source_path)
    save_json_file(target_path, official_dict, indent=2)
    return official_dict, target_path


def load_official_dict(resource_path_file):
    official_dict = load_json_file(resource_path_file, default=empty_custom_dict())
    return ensure_custom_dict_schema(official_dict if isinstance(official_dict, dict) else empty_custom_dict())


def load_effective_dict(dict_path):
    effective_dict = load_json_file(dict_path, default=empty_custom_dict())
    return ensure_custom_dict_schema(effective_dict if isinstance(effective_dict, dict) else empty_custom_dict())


def save_custom_dict(dict_path, custom_dict):
    save_json_file(dict_path, ensure_custom_dict_schema(custom_dict), indent=2)


def save_effective_dict(dict_path, effective_dict):
    save_json_file(dict_path, ensure_custom_dict_schema(effective_dict), indent=2)


def _as_list(value):
    if isinstance(value, (list, tuple, set)):
        return list(value)
    if value is None:
        return []
    return [value]


def _merge_unique_values(existing_values, incoming_values):
    merged = []
    for value in _as_list(existing_values) + _as_list(incoming_values):
        if value not in merged:
            merged.append(value)
    return merged


def merge_dict_payload(base_dict, new_dict):
    merged = ensure_custom_dict_schema(dict(base_dict) if isinstance(base_dict, dict) else {})
    incoming = ensure_custom_dict_schema(dict(new_dict) if isinstance(new_dict, dict) else {})

    merged["normal_words"] = {**merged["normal_words"], **incoming.get("normal_words", {})}
    merged["compound_words"] = {**merged["compound_words"], **incoming.get("compound_words", {})}

    for key in ("suffix_combinations", "prefix_combinations"):
        for word, items in incoming.get(key, {}).items():
            incoming_values = _as_list(items)
            if not incoming_values:
                merged[key][word] = []
                continue
            if word in merged[key]:
                merged[key][word] = _merge_unique_values(merged[key][word], incoming_values)
            else:
                merged[key][word] = incoming_values

    return merged


def import_dict_file(current_dict, file_path):
    new_dict = load_json_file(file_path, default=None)
    if not isinstance(new_dict, dict):
        raise ValueError("invalid dictionary json")
    return merge_dict_payload(current_dict, new_dict)
