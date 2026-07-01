APP_VERSION = "0.4.0"

CONFIG_SCHEMA_VERSION = 2

DICT_MERGE_POLICY_ASK = "ask"
DICT_MERGE_POLICY_KEEP_LOCAL = "keep_local"
DICT_MERGE_POLICY_REPLACE_OFFICIAL = "replace_official"
DEFAULT_DICT_MERGE_POLICY = DICT_MERGE_POLICY_ASK

DEFAULT_APP_CONFIG = {
    "current_dict_path": None,
    "minimize_to_tray_without_asking": False,
    "close_action": "minimize",
    "entries_per_page": 20,
    "enable_conflict_detection": True,
    "official_dict_merge_policy": DEFAULT_DICT_MERGE_POLICY,
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


def normalize_dict_merge_policy(policy):
    if policy in (
        DICT_MERGE_POLICY_ASK,
        DICT_MERGE_POLICY_KEEP_LOCAL,
        DICT_MERGE_POLICY_REPLACE_OFFICIAL,
    ):
        return policy
    return DEFAULT_DICT_MERGE_POLICY


def normalize_app_config(raw_config):
    raw_config = raw_config if isinstance(raw_config, dict) else {}
    payload = {key: value for key, value in raw_config.items() if not _is_meta_key(key)}
    normalized = _merge_dicts(default_app_config(), payload)
    normalized["official_dict_merge_policy"] = normalize_dict_merge_policy(
        normalized.get("official_dict_merge_policy")
    )
    normalized["_schema_version"] = CONFIG_SCHEMA_VERSION
    normalized["_app_version"] = APP_VERSION

    for key, value in raw_config.items():
        if _is_meta_key(key) and key not in normalized:
            normalized[key] = value

    return normalized


def merge_app_config(existing_config, updates):
    merged = _merge_dicts(existing_config, updates)
    return normalize_app_config(merged)
