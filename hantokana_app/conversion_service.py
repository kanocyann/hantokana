from .conversion_core import (
    ensure_custom_dict_schema,
    extract_hira_reading,
    format_reading_line,
    has_japanese_chars,
    iter_non_overlapping_occurrences,
)
from .conversion_pipeline import (
    expand_combination_words,
    build_tokenized_words,
    detect_conflicts,
    resolve_direct_readings,
)


def convert_text_payload(raw_text, custom_dict, tagger, conv, use_hira, use_kata, use_roma, romaji_converter, conflict_detection=True):
    raw = (raw_text or "").strip()
    if not raw:
        return "请输入日文文本。"
    if not (use_hira or use_kata or use_roma):
        return "请选择至少一个转换方式"

    custom_dict = ensure_custom_dict_schema(custom_dict)
    prefix_combinations = custom_dict.get("prefix_combinations", {})
    suffix_combinations = custom_dict.get("suffix_combinations", {})
    compound_words = custom_dict.get("compound_words", {})
    normal_words = custom_dict.get("normal_words", {})

    direct_words = sorted(set(normal_words) | set(compound_words), key=len, reverse=True)
    prefix_combination_words = expand_combination_words(prefix_combinations, bidirectional=True)
    suffix_combination_words = expand_combination_words(suffix_combinations)

    processed_ranges = []
    processed_words = set()
    result_entries = []

    processed_direct_matches = []
    for word in direct_words:
        readings = resolve_direct_readings(word, compound_words, normal_words)
        if not readings:
            continue
        for position in iter_non_overlapping_occurrences(raw, word, processed_ranges):
            line = format_reading_line(word, readings, use_hira, use_kata, use_roma, romaji_converter)
            processed_ranges.append((position, position + len(word)))
            processed_words.add(word)
            processed_direct_matches.append((position, line, word))

    words = tagger(raw)

    processed_combinations = []
    for word in prefix_combination_words:
        readings = _lookup_readings(conv, word)
        if not readings:
            continue
        for position in iter_non_overlapping_occurrences(raw, word, processed_ranges):
            line = format_reading_line(word, readings, use_hira, use_kata, use_roma, romaji_converter)
            processed_ranges.append((position, position + len(word)))
            processed_words.add(word)
            processed_combinations.append((position, line, word))

    for combined in suffix_combination_words:
        readings = _lookup_readings(
            conv,
            combined,
            normal_words.get(combined) or compound_words.get(combined),
        )
        if not readings:
            continue
        for position in iter_non_overlapping_occurrences(raw, combined, processed_ranges):
            line = format_reading_line(combined, readings, use_hira, use_kata, use_roma, romaji_converter)
            processed_ranges.append((position, position + len(combined)))
            processed_words.add(combined)
            processed_combinations.append((position, line, combined))

    tokenized_words = build_tokenized_words(
        words,
        prefix_combinations,
        suffix_combinations,
        compound_words,
    )
    for word in tokenized_words:
        if not has_japanese_chars(word):
            continue

        readings = _lookup_readings(conv, word, normal_words.get(word) or compound_words.get(word))
        if not readings:
            continue
        for position in iter_non_overlapping_occurrences(raw, word, processed_ranges):
            line = format_reading_line(word, readings, use_hira, use_kata, use_roma, romaji_converter)
            processed_ranges.append((position, position + len(word)))
            processed_words.add(word)
            result_entries.append((position, line, word))

    result_entries.extend(processed_direct_matches)
    result_entries.extend(processed_combinations)
    result_entries.sort(key=lambda item: item[0])

    result = "\n".join(entry[1] for entry in result_entries)
    if conflict_detection:
        conflict_report = detect_conflicts(raw, processed_ranges, processed_words, tagger)
        if conflict_report:
            result += "\n\n" + conflict_report

    return result.strip()


def _lookup_readings(conv, word, fallback_readings=None):
    if fallback_readings:
        if isinstance(fallback_readings, (list, tuple)):
            return list(fallback_readings)
        return [fallback_readings]

    converted = conv.convert(word)
    reading = extract_hira_reading(converted)
    if reading:
        return [reading]
    return []
