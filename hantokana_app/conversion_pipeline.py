from .conversion_core import has_japanese_chars


def resolve_direct_readings(word, compound_words, normal_words):
    readings = normal_words.get(word) or compound_words.get(word)
    if not readings:
        return []
    if isinstance(readings, (list, tuple)):
        return list(readings)
    return [readings]


def expand_combination_words(combination_map, bidirectional=False):
    words = []
    seen = set()

    for first, seconds in (combination_map or {}).items():
        for second in seconds:
            combined = first + second
            if combined not in seen:
                seen.add(combined)
                words.append(combined)

            if bidirectional:
                reverse_combined = second + first
                if reverse_combined not in seen:
                    seen.add(reverse_combined)
                    words.append(reverse_combined)

    return sorted(words, key=len, reverse=True)


def build_combination_pairs(combination_map, bidirectional=False):
    pairs = set()

    for first, seconds in (combination_map or {}).items():
        for second in seconds:
            pairs.add((first, second))
            if bidirectional:
                pairs.add((second, first))

    return pairs


def build_tokenized_words(words, prefix_combinations, suffix_combinations, compound_words):
    tokenized_words = []
    index = 0
    prefix_pairs = build_combination_pairs(prefix_combinations, bidirectional=True)
    suffix_pairs = build_combination_pairs(suffix_combinations)

    while index < len(words):
        current_word = words[index].surface

        for end in range(len(words), index, -1):
            combined = "".join(word.surface for word in words[index:end])
            if combined in compound_words:
                tokenized_words.append(combined)
                index = end
                break
        else:
            if index + 1 < len(words):
                next_word = words[index + 1].surface

                if (current_word, next_word) in prefix_pairs:
                    tokenized_words.append(current_word + next_word)
                    index += 2
                    continue

                if (current_word, next_word) in suffix_pairs:
                    tokenized_words.append(current_word + next_word)
                    index += 2
                    continue

                if current_word.endswith(("っ", "ッ")):
                    tokenized_words.append(current_word + next_word)
                    index += 2
                else:
                    tokenized_words.append(current_word)
                    index += 1
            else:
                tokenized_words.append(current_word)
                index += 1

    return tokenized_words


def detect_conflicts(raw_text, processed_ranges, processed_words, tagger):
    if len(raw_text) < 2 or not processed_ranges:
        return ""

    sorted_ranges = sorted(processed_ranges)

    unprocessed_ranges = []
    last_end = 0

    for start, end in sorted_ranges:
        if start > last_end:
            unprocessed_ranges.append((last_end, start))
        last_end = max(last_end, end)

    if last_end < len(raw_text):
        unprocessed_ranges.append((last_end, len(raw_text)))

    if not unprocessed_ranges:
        return ""

    unprocessed_texts = [raw_text[start:end] for start, end in unprocessed_ranges]
    unprocessed_texts = [text for text in unprocessed_texts if text.strip()]
    if not unprocessed_texts:
        return ""

    if not any(has_japanese_chars(text) for text in unprocessed_texts):
        return ""

    potential_conflicts = []

    for text in unprocessed_texts:
        if not text.strip() or not has_japanese_chars(text):
            continue

        try:
            words = tagger(text)
            for word in words:
                surface = word.surface
                if not surface.strip() or not has_japanese_chars(surface):
                    continue
                if surface not in processed_words and len(surface) > 1:
                    potential_conflicts.append(surface)
        except Exception:
            continue

    if not potential_conflicts:
        return ""

    unique_conflicts = sorted(set(potential_conflicts), key=len, reverse=True)
    max_conflicts = 10

    conflict_report = "【词典规则冲突检测报告】\n"
    conflict_report += "以下词汇可能因为规则冲突而未被正确处理：\n"
    if len(unique_conflicts) > max_conflicts:
        conflict_report += ", ".join(unique_conflicts[:max_conflicts]) + f"... 等{len(unique_conflicts)}个词汇"
    else:
        conflict_report += ", ".join(unique_conflicts)

    conflict_report += "\n\n请检查您的词典规则是否存在冲突，或者将这些词汇添加到适当的词典中。"
    return conflict_report
