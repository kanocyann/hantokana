import jaconv


DICT_KEYS = ("normal_words", "compound_words", "prefix_combinations", "suffix_combinations")


def empty_custom_dict():
    return {key: {} for key in DICT_KEYS}


def ensure_custom_dict_schema(custom_dict):
    if not isinstance(custom_dict, dict):
        custom_dict = {}
    for key in DICT_KEYS:
        if not isinstance(custom_dict.get(key), dict):
            custom_dict[key] = {}
    return custom_dict


def has_japanese_chars(text):
    text = "" if text is None else str(text)
    return any(
        0x3040 <= ord(char) <= 0x309F
        or 0x30A0 <= ord(char) <= 0x30FF
        or 0x4E00 <= ord(char) <= 0x9FFF
        for char in text
    )


def ranges_overlap(start, end, existing_start, existing_end):
    return (
        existing_start <= start < existing_end
        or existing_start < end <= existing_end
        or start <= existing_start < end
    )


def is_range_processed(processed_ranges, start, length):
    end = start + length
    return any(ranges_overlap(start, end, processed_start, processed_end) for processed_start, processed_end in processed_ranges)


def iter_non_overlapping_occurrences(text, needle, processed_ranges, shadowed_matches=None, source=None):
    if not text or not needle:
        return

    start_pos = 0
    while True:
        pos = text.find(needle, start_pos)
        if pos == -1:
            break
        if is_range_processed(processed_ranges, pos, len(needle)):
            if shadowed_matches is not None:
                shadowed_matches.append({
                    "word": needle,
                    "position": pos,
                    "end": pos + len(needle),
                    "source": source,
                })
            start_pos = pos + 1
            continue
        yield pos
        start_pos = pos + 1


def extract_hira_reading(converted):
    if not converted:
        return ""
    return "".join(item.get("hira", item.get("orig", "")) for item in converted)


def format_reading_line(word, readings, use_hira, use_kata, use_roma, romaji_converter):
    line = f"[{word}]"
    normalized = [jaconv.kata2hira(str(reading)) for reading in readings if str(reading)]

    if use_hira:
        line += f" → [{', '.join(normalized)}]"

    if use_kata:
        kata_readings = [jaconv.hira2kata(reading) for reading in normalized]
        line += f" → [{', '.join(kata_readings)}]"

    if use_roma:
        roma_readings = [romaji_converter(reading, word) for reading in normalized]
        line += f" → [{', '.join(roma_readings)}]"

    return line


BASIC_ROMAJI = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "wi", "ゑ": "we", "を": "wo", "ん": "n",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
    "ゔ": "vu",
}


YOON_ROMAJI = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    "しぇ": "she", "ちぇ": "che", "じぇ": "je",
    "てぃ": "ti", "でぃ": "di", "とぅ": "tu", "どぅ": "du",
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo",
    "ゔぁ": "va", "ゔぃ": "vi", "ゔぇ": "ve", "ゔぉ": "vo",
}


def _first_vowel(romaji):
    for char in reversed(romaji):
        if char in "aeiou":
            return char
    return ""


def _sokuon_prefix(next_romaji):
    if not next_romaji:
        return ""
    if next_romaji.startswith(("ch", "ts")):
        return "t"
    if next_romaji.startswith("sh"):
        return "s"
    if next_romaji[0] in "aeiou":
        return ""
    return next_romaji[0]


def _apply_particle_readings(tokens, kana_text, surface_text):
    if not tokens:
        return tokens

    surface = surface_text or kana_text
    if not surface:
        return tokens

    if surface.endswith("は") and kana_text.endswith("は"):
        tokens[-1] = "wa"
    elif surface.endswith("へ") and kana_text.endswith("へ"):
        tokens[-1] = "e"
    elif surface.endswith("を") and kana_text.endswith("を"):
        tokens[-1] = "o"
    return tokens


def kana_to_romaji(kana_text, surface_text=None):
    hira = jaconv.kata2hira(str(kana_text))
    tokens = []
    pending_sokuon = False
    i = 0

    while i < len(hira):
        char = hira[i]

        if char in ("っ", "ッ"):
            pending_sokuon = True
            i += 1
            continue

        if char == "ー":
            vowel = _first_vowel(tokens[-1]) if tokens else ""
            if vowel:
                tokens[-1] += vowel
            else:
                tokens.append("-")
            i += 1
            continue

        if char == "ん":
            next_char = hira[i + 1] if i + 1 < len(hira) else ""
            if next_char and (next_char in "あいうえおやゆよ" or next_char == "ん"):
                token = "n'"
            else:
                token = "n"
            tokens.append(token)
            i += 1
            continue

        combo = hira[i:i + 2]
        if combo in YOON_ROMAJI:
            token = YOON_ROMAJI[combo]
            i += 2
        else:
            token = BASIC_ROMAJI.get(char, char)
            i += 1

        if pending_sokuon:
            token = _sokuon_prefix(token) + token
            pending_sokuon = False

        tokens.append(token)

    if pending_sokuon:
        tokens.append("t")

    tokens = _apply_particle_readings(tokens, hira, jaconv.kata2hira(str(surface_text)) if surface_text else None)
    return "".join(tokens)
