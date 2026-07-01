import json
import os
import sys
import hashlib
from pathlib import Path

from .conversion_core import empty_custom_dict, ensure_custom_dict_schema
from .app_config import APP_VERSION, merge_app_config, normalize_app_config, normalize_dict_merge_policy


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


def get_config_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "config.json")


def get_official_dict_state_path(app_name=APP_NAME):
    return os.path.join(get_appdata_path(app_name), "official_dict_state.json")


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


def load_official_dict_state(state_path):
    state = load_json_file(state_path, default={})
    return state if isinstance(state, dict) else {}


def save_official_dict_state(state_path, state):
    payload = state if isinstance(state, dict) else {}
    save_json_file(state_path, payload, indent=4)


def official_dict_needs_sync(state_path, resource_path_file):
    state = load_official_dict_state(state_path)
    current_hash = compute_file_sha256(resource_path_file)
    if not current_hash:
        return False
    return state.get("sha256") != current_hash


def load_custom_dict(dict_path, initial_resource_path=None):
    if not os.path.exists(dict_path):
        if initial_resource_path and os.path.exists(initial_resource_path):
            _ensure_parent_dir(dict_path)
            with open(initial_resource_path, "r", encoding="utf-8") as src:
                data = src.read()
            with open(dict_path, "w", encoding="utf-8") as dst:
                dst.write(data)
        else:
            save_json_file(dict_path, empty_custom_dict(), indent=2)

    custom_dict = ensure_custom_dict_schema(load_json_file(dict_path, default=empty_custom_dict()))
    return custom_dict, dict_path


def load_official_dict(resource_path_file):
    official_dict = load_json_file(resource_path_file, default=empty_custom_dict())
    return ensure_custom_dict_schema(official_dict if isinstance(official_dict, dict) else empty_custom_dict())


def compute_file_sha256(path):
    if not path or not os.path.exists(path):
        return ""

    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def save_custom_dict(dict_path, custom_dict):
    save_json_file(dict_path, ensure_custom_dict_schema(custom_dict), indent=2)


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
            if word in merged[key]:
                merged[key][word] = _merge_unique_values(merged[key][word], items)
            else:
                merged[key][word] = _as_list(items)

    return merged


def import_dict_file(current_dict, file_path):
    new_dict = load_json_file(file_path, default=None)
    if not isinstance(new_dict, dict):
        raise ValueError("invalid dictionary json")
    return merge_dict_payload(current_dict, new_dict)


def merge_string_lists(existing_values, incoming_values):
    return _merge_unique_values(existing_values, incoming_values)


def merge_official_and_local_dicts(official_dict, local_dict, policy=None):
    official = ensure_custom_dict_schema(dict(official_dict) if isinstance(official_dict, dict) else {})
    local = ensure_custom_dict_schema(dict(local_dict) if isinstance(local_dict, dict) else {})

    effective_policy = normalize_dict_merge_policy(policy)
    merged = empty_custom_dict()
    conflicts = []
    changed_keys = []

    for key in ("normal_words", "compound_words"):
        official_bucket = official.get(key, {})
        local_bucket = local.get(key, {})
        merged_bucket = {}
        all_words = sorted(set(official_bucket) | set(local_bucket))

        for word in all_words:
            official_value = official_bucket.get(word)
            local_value = local_bucket.get(word)

            if official_value is None:
                merged_bucket[word] = local_value
                continue

            if local_value is None:
                merged_bucket[word] = official_value
                continue

            if official_value == local_value:
                merged_bucket[word] = local_value
                continue

            changed_keys.append((key, word))
            conflicts.append({
                "group": key,
                "word": word,
                "official": official_value,
                "local": local_value,
            })

            if effective_policy == "replace_official":
                merged_bucket[word] = official_value
            elif effective_policy == "keep_local":
                merged_bucket[word] = local_value
            else:
                merged_bucket[word] = local_value

        merged[key] = merged_bucket

    for key in ("prefix_combinations", "suffix_combinations"):
        official_bucket = official.get(key, {})
        local_bucket = local.get(key, {})
        merged_bucket = {}
        all_words = sorted(set(official_bucket) | set(local_bucket))

        for word in all_words:
            official_value = official_bucket.get(word)
            local_value = local_bucket.get(word)

            if official_value is None:
                merged_bucket[word] = local_value
                continue

            if local_value is None:
                merged_bucket[word] = official_value
                continue

            merged_values = merge_string_lists(official_value, local_value)
            merged_bucket[word] = merged_values
            if merged_values != official_value or merged_values != local_value:
                changed_keys.append((key, word))

            if official_value != local_value:
                conflicts.append({
                    "group": key,
                    "word": word,
                    "official": official_value,
                    "local": local_value,
                })

        merged[key] = merged_bucket

    return {
        "merged_dict": ensure_custom_dict_schema(merged),
        "conflicts": conflicts,
        "changed_keys": changed_keys,
        "policy": effective_policy,
    }


def build_official_dict_snapshot(resource_path_file, official_dict=None, version=APP_VERSION):
    return {
        "version": version,
        "sha256": compute_file_sha256(resource_path_file),
        "path": resource_path_file,
        "dict": ensure_custom_dict_schema(official_dict if isinstance(official_dict, dict) else empty_custom_dict()),
    }
