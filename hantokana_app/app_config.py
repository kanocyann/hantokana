APP_VERSION = "0.4.1"

CONFIG_SCHEMA_VERSION = 3

DEFAULT_APP_CONFIG = {
    "current_dict_path": None,
    "minimize_to_tray_without_asking": False,
    "close_action": "minimize",
    "entries_per_page": 20,
    "enable_conflict_detection": False,
}


def default_app_config():
    return dict(DEFAULT_APP_CONFIG)


def _is_meta_key(key):
    return isinstance(key, str) and key.startswith("_")


def _merge_dicts(base, incoming):
    merged = dict(base) if isinstance(base, dict) else {}
    if not isinstance(incoming, dict):
        return merged

    for key, value in incoming.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def _merge_known_fields(defaults, raw_values):
    normalized = dict(defaults) if isinstance(defaults, dict) else {}
    if not isinstance(raw_values, dict):
        return normalized

    for key, default_value in defaults.items():
        if key not in raw_values:
            continue

        raw_value = raw_values[key]
        if isinstance(default_value, dict):
            normalized[key] = _merge_known_fields(default_value, raw_value)
        else:
            normalized[key] = raw_value
    return normalized


def normalize_app_config(raw_config):
    raw_config = raw_config if isinstance(raw_config, dict) else {}
    normalized = _merge_known_fields(default_app_config(), raw_config)

    normalized["_schema_version"] = CONFIG_SCHEMA_VERSION
    normalized["_app_version"] = APP_VERSION

    return normalized


def merge_app_config(existing_config, updates):
    base_config = normalize_app_config(existing_config)
    clean_updates = {}
    if isinstance(updates, dict):
        clean_updates = {
            key: value
            for key, value in updates.items()
            if key in DEFAULT_APP_CONFIG or _is_meta_key(key)
        }
    merged = _merge_dicts(base_config, clean_updates)
    return normalize_app_config(merged)
