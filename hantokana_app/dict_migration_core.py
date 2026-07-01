from .conversion_core import empty_custom_dict, ensure_custom_dict_schema


DICT_GROUP_ORDER = (
    "normal_words",
    "compound_words",
    "prefix_combinations",
    "suffix_combinations",
)

PREFIX_SUFFIX_GROUPS = {"prefix_combinations", "suffix_combinations"}

GROUP_LABELS = {
    "normal_words": "普通词",
    "compound_words": "复合词",
    "prefix_combinations": "前缀组合",
    "suffix_combinations": "后缀组合",
}

ACTION_LABELS = {
    "keep_local": "保留本地",
    "use_official": "采用云端",
    "merge": "合并",
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


def _format_values(value):
    return ", ".join(str(item) for item in value or [])


def _classify(base_present, base_value, local_present, local_value, official_present, official_value):
    if local_present and official_present and local_value == official_value:
        if base_present and base_value == local_value:
            return None
        return "shared"

    if not base_present:
        if local_present and official_present:
            return "conflict_new"
        if local_present:
            return "local_only"
        if official_present:
            return "official_only"
        return None

    if local_present and official_present:
        return "conflict"
    if local_present and not official_present:
        return "local_only"
    if official_present and not local_present:
        return "official_only"
    return "deleted"


def _recommended_action(change_type):
    if change_type == "official_only":
        return "use_official"
    if change_type == "local_only":
        return "keep_local"
    if change_type in ("shared", "deleted"):
        return "merge"
    return "merge"


def _default_action(change_type, policy):
    if policy == "keep_local":
        return "keep_local"
    if policy == "replace_official":
        return "use_official"
    return _recommended_action(change_type)


def build_official_dict_sync_plan(state_snapshot, local_dict, official_dict, policy="ask"):
    state_dict = normalize_custom_dict_payload((state_snapshot or {}).get("dict"))
    local = normalize_custom_dict_payload(local_dict)
    official = normalize_custom_dict_payload(official_dict)
    has_state = bool((state_snapshot or {}).get("sha256")) or bool((state_snapshot or {}).get("dict"))

    items = []
    counts = {}

    for group in DICT_GROUP_ORDER:
        state_bucket = state_dict.get(group, {})
        local_bucket = local.get(group, {})
        official_bucket = official.get(group, {})
        all_words = sorted(set(state_bucket) | set(local_bucket) | set(official_bucket))

        for word in all_words:
            base_present = word in state_bucket
            local_present = word in local_bucket
            official_present = word in official_bucket
            base_value = state_bucket.get(word)
            local_value = local_bucket.get(word)
            official_value = official_bucket.get(word)

            change_type = _classify(
                base_present,
                base_value,
                local_present,
                local_value,
                official_present,
                official_value,
            )

            if change_type == "shared":
                counts[change_type] = counts.get(change_type, 0) + 1
                continue

            if not has_state and not local_present and official_present:
                change_type = "official_only"
            elif not has_state and local_present and not official_present:
                change_type = "local_only"
            elif not has_state and local_present and official_present and local_value != official_value:
                change_type = "conflict_new"

            if change_type is None:
                continue

            item = {
                "group": group,
                "group_label": GROUP_LABELS[group],
                "word": word,
                "base_present": base_present,
                "local_present": local_present,
                "official_present": official_present,
                "base": base_value,
                "local": local_value,
                "official": official_value,
                "change_type": change_type,
                "change_label": change_type,
                "recommended_action": _recommended_action(change_type),
                "default_action": _default_action(change_type, policy),
                "is_conflict": change_type in ("conflict", "conflict_new"),
                "is_prefix_suffix": group in PREFIX_SUFFIX_GROUPS,
            }
            items.append(item)
            counts[change_type] = counts.get(change_type, 0) + 1

    summary = {
        "total": len(items),
        "conflicts": counts.get("conflict", 0) + counts.get("conflict_new", 0),
        "official_only": counts.get("official_only", 0),
        "local_only": counts.get("local_only", 0),
        "shared": counts.get("shared", 0),
        "deleted": counts.get("deleted", 0),
    }

    return {
        "state_snapshot": state_snapshot if isinstance(state_snapshot, dict) else {},
        "local_dict": local,
        "official_dict": official,
        "items": items,
        "counts": counts,
        "summary": summary,
        "policy": policy,
        "has_state": has_state,
    }


def _merge_value(local_value, official_value, action):
    if action == "keep_local":
        return None if local_value is None else list(local_value)
    if action == "use_official":
        return None if official_value is None else list(official_value)

    merged = []
    for value in (local_value, official_value):
        if value is None:
            continue
        for item in value:
            if item not in merged:
                merged.append(item)
    return merged if merged else None


def resolve_official_dict_sync(plan, decisions=None):
    decisions = decisions if isinstance(decisions, dict) else {}
    merged = empty_custom_dict()
    local_dict = plan.get("local_dict") or empty_custom_dict()

    for group in DICT_GROUP_ORDER:
        merged[group] = dict(local_dict.get(group, {}))

    for item in plan.get("items", []):
        key = (item["group"], item["word"])
        action = decisions.get(key, item.get("default_action") or item.get("recommended_action") or "merge")
        value = _merge_value(item.get("local"), item.get("official"), action)
        bucket = merged.setdefault(item["group"], {})
        if value is None:
            bucket.pop(item["word"], None)
        else:
            bucket[item["word"]] = value

    return ensure_custom_dict_schema(merged)


def action_label(action):
    return ACTION_LABELS.get(action, action)
