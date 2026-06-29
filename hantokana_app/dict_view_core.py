DICT_TYPE_META = {
    "normal_words": {
        "dialog_title": "普通词",
        "word_label": "汉字",
        "word_placeholder": "请输入汉字或词汇",
        "reading_label": "对应假名 (用逗号间隔)",
        "reading_placeholder": "请输入假名读音，多个读音用逗号分隔",
        "display_name": "普通词",
    },
    "compound_words": {
        "dialog_title": "复合词",
        "word_label": "复合词",
        "word_placeholder": "请输入复合词",
        "reading_label": "对应假名 (用逗号间隔)",
        "reading_placeholder": "请输入假名读音，多个读音用逗号分隔",
        "display_name": "复合词",
    },
    "prefix_combinations": {
        "dialog_title": "常见前缀组合",
        "word_label": "助词 (前接词汇)",
        "word_placeholder": "请输入助词 (如: まで、から等)",
        "reading_label": "对应词汇 (用逗号间隔)",
        "reading_placeholder": "请输入词汇，多个词汇用逗号分隔",
        "display_name": "前缀组合",
    },
    "suffix_combinations": {
        "dialog_title": "常见后缀组合",
        "word_label": "词汇 (后接助词)",
        "word_placeholder": "请输入词汇 (如: それ、これ等)",
        "reading_label": "对应助词 (用逗号间隔)",
        "reading_placeholder": "请输入助词，多个助词用逗号分隔",
        "display_name": "后缀组合",
    },
}

DICT_TYPE_ORDER = tuple(DICT_TYPE_META.keys())
DICT_SEARCH_TYPES = ("全部",) + tuple(meta["display_name"] for meta in DICT_TYPE_META.values())
DISPLAY_NAME_TO_WORD_TYPE = {meta["display_name"]: key for key, meta in DICT_TYPE_META.items()}

DEFAULT_DICT_TYPE_META = {
    "dialog_title": "自定义",
    "word_label": "词条",
    "word_placeholder": "请输入词条",
    "reading_label": "对应内容 (用逗号间隔)",
    "reading_placeholder": "请输入内容，多个值用逗号分隔",
    "display_name": "自定义",
}


def get_dict_type_meta(word_type):
    return dict(DICT_TYPE_META.get(word_type, DEFAULT_DICT_TYPE_META))


def format_dict_value_text(value):
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def iter_custom_dict_entries(custom_dict):
    data = custom_dict if isinstance(custom_dict, dict) else {}
    for word_type in DICT_TYPE_ORDER:
        display_name = DICT_TYPE_META[word_type]["display_name"]
        for word, readings in data.get(word_type, {}).items():
            yield {
                "word": word,
                "readings": format_dict_value_text(readings),
                "type": display_name,
            }


def split_search_keywords(search_text):
    if not search_text:
        return []
    return [keyword.strip().lower() for keyword in str(search_text).split() if keyword.strip()]


def entry_matches_filters(entry, current_type="全部", search_keywords=None):
    if not isinstance(entry, dict):
        return False

    if current_type != "全部" and entry.get("type") != current_type:
        return False

    keywords = [keyword for keyword in (search_keywords or []) if keyword]
    if not keywords:
        return True

    word = str(entry.get("word", "")).lower()
    readings = str(entry.get("readings", "")).lower()
    haystack = f"{word} {readings}"
    return all(keyword in haystack for keyword in keywords)


def _merge_spans(spans):
    if not spans:
        return []

    merged = [spans[0]]
    for start, end in spans[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def highlight_text(text, search_keywords, highlight_color="#FFFF00"):
    text = "" if text is None else str(text)
    keywords = [keyword for keyword in (search_keywords or []) if keyword]
    if not text or not keywords:
        return text

    lower_text = text.lower()
    matches = []
    for keyword in keywords:
        pos = 0
        while True:
            pos = lower_text.find(keyword, pos)
            if pos == -1:
                break
            matches.append((pos, pos + len(keyword)))
            pos += 1

    if not matches:
        return text

    matches.sort()
    merged_matches = _merge_spans(matches)

    result = ""
    last_end = 0
    for start, end in merged_matches:
        result += text[last_end:start]
        result += f'<span style="background-color: {highlight_color};">{text[start:end]}</span>'
        last_end = end
    result += text[last_end:]
    return result
