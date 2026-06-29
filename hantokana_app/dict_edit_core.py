from .dict_view_core import format_dict_value_text


ENTRY_SEPARATOR = " → "
VALUE_SEPARATORS = (",", "，", "、")


def split_entry_values(raw):
    """Split a comma-like separated dictionary value string."""
    text = "" if raw is None else str(raw)
    for sep in VALUE_SEPARATORS:
        text = text.replace(sep, ",")
    return [value.strip() for value in text.split(",") if value.strip()]


def ensure_entry_bucket(custom_dict, word_type):
    if not isinstance(custom_dict, dict):
        raise TypeError("custom_dict must be a dict")
    if not isinstance(custom_dict.get(word_type), dict):
        custom_dict[word_type] = {}
    return custom_dict[word_type]


def iter_edit_entries(custom_dict, word_type):
    bucket = ensure_entry_bucket(custom_dict, word_type)
    for word, values in sorted(bucket.items()):
        yield word, values


def format_entry_text(word, values):
    return f"{word}{ENTRY_SEPARATOR}{format_dict_value_text(values)}"


def parse_entry_display_text(text):
    text = "" if text is None else str(text)
    if ENTRY_SEPARATOR not in text:
        return text, ""
    word, values = text.split(ENTRY_SEPARATOR, 1)
    return word, values


def set_dict_entry(custom_dict, word_type, word, values):
    bucket = ensure_entry_bucket(custom_dict, word_type)
    existed = word in bucket
    bucket[word] = list(values)
    return existed


def delete_dict_entries(custom_dict, word_type, words):
    bucket = ensure_entry_bucket(custom_dict, word_type)
    deleted = 0
    for word in words:
        if word in bucket:
            del bucket[word]
            deleted += 1
    return deleted
