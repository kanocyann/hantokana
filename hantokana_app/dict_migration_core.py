from .conversion_core import empty_custom_dict, ensure_custom_dict_schema


DICT_GROUP_ORDER = (
    "normal_words",
    "compound_words",
    "prefix_combinations",
    "suffix_combinations",
)

SOURCE_OFFICIAL = "official"
SOURCE_CUSTOM = "custom"
SOURCE_OVERRIDE = "override"
SOURCE_DELETED = "deleted"
SOURCE_MISSING = "missing"

SOURCE_LABELS = {
    SOURCE_OFFICIAL: "官方",
    SOURCE_CUSTOM: "我的",
    SOURCE_OVERRIDE: "已修改",
    SOURCE_DELETED: "已删除",
    SOURCE_MISSING: "未找到",
}


def _dedupe(values):
    merged = []
    for value in values or []:
        if value not in merged:
            merged.append(value)
    return merged


def _normalize_value(value):
    if isinstance(value, (list, tuple, set)):
        return _dedupe(list(value))
    if value is None:
        return []
    return [value]


def normalize_custom_dict_payload(custom_dict):
    payload = ensure_custom_dict_schema(dict(custom_dict) if isinstance(custom_dict, dict) else {})
    normalized = empty_custom_dict()
    for group in DICT_GROUP_ORDER:
        bucket = {}
        for word, value in payload.get(group, {}).items():
            bucket[word] = _normalize_value(value)
        normalized[group] = bucket
    return normalized


def is_deleted_marker(value):
    return _normalize_value(value) == []


def merge_official_and_custom_dicts(official_dict, custom_dict):
    official = normalize_custom_dict_payload(official_dict)
    custom = normalize_custom_dict_payload(custom_dict)
    merged = empty_custom_dict()

    for group in DICT_GROUP_ORDER:
        merged[group] = dict(official.get(group, {}))
        for word, local_value in custom.get(group, {}).items():
            if is_deleted_marker(local_value):
                merged[group].pop(word, None)
                continue
            merged[group][word] = local_value

    return ensure_custom_dict_schema(merged)


def prune_redundant_custom_entries(official_dict, custom_dict):
    official = normalize_custom_dict_payload(official_dict)
    custom = normalize_custom_dict_payload(custom_dict)
    pruned = empty_custom_dict()

    for group in DICT_GROUP_ORDER:
        official_bucket = official.get(group, {})
        for word, custom_value in custom.get(group, {}).items():
            if is_deleted_marker(custom_value):
                pruned[group][word] = []
                continue
            if word in official_bucket and custom_value == official_bucket[word]:
                continue
            pruned[group][word] = custom_value

    return ensure_custom_dict_schema(pruned), pruned != custom


def build_effective_dict_cache(official_dict, custom_dict):
    return merge_official_and_custom_dicts(official_dict, custom_dict)


def dict_entry_source(official_dict, custom_dict, group, word):
    official = normalize_custom_dict_payload(official_dict)
    custom = normalize_custom_dict_payload(custom_dict)
    in_official = word in official.get(group, {})
    in_custom = word in custom.get(group, {})
    custom_value = custom.get(group, {}).get(word)

    if in_custom and is_deleted_marker(custom_value):
        return SOURCE_DELETED
    if in_official and in_custom:
        return SOURCE_OVERRIDE
    if in_custom:
        return SOURCE_CUSTOM
    if in_official:
        return SOURCE_OFFICIAL
    return SOURCE_MISSING


def source_label(source):
    return SOURCE_LABELS.get(source, source)
