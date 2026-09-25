import unittest

from hantokana_app.conversion_core import ensure_custom_dict_schema, format_reading_line, kana_to_romaji
from hantokana_app.conversion_service import convert_text_payload


class _DummyTagger:
    def __call__(self, text):
        return []


class _DummyConv:
    def convert(self, word):
        return [{"hira": word}]


class _DummyFeature:
    def __init__(self, pos1, kana, pron):
        self.pos1 = pos1
        self.kana = kana
        self.pron = pron


class _DummyToken:
    def __init__(self, surface, pos1="名詞", kana="", pron="", white_space=""):
        self.surface = surface
        self.feature = _DummyFeature(pos1, kana, pron)
        self.white_space = white_space


class _ParticleAwareTagger:
    tokens_by_text = {
        "は": [_DummyToken("は", "助詞", "ハ", "ワ")],
        "はは": [_DummyToken("はは", "感動詞", "ハハ", "ハハ")],
        "ははは": [_DummyToken("ははは", "感動詞", "ハハハ", "ハハハ")],
        "それでは": [
            _DummyToken("それ", "代名詞", "ソレ", "ソレ"),
            _DummyToken("で", "助詞", "デ", "デ"),
            _DummyToken("は", "助詞", "ハ", "ワ"),
        ],
        "こんにちは": [_DummyToken("こんにちは", "感動詞", "コンニチハ", "コンニチワ")],
        "こんにち\nは": [
            _DummyToken("こんにち", "名詞", "コンニチ", "コンニチ"),
            _DummyToken("は", "助詞", "ハ", "ワ", white_space="\n"),
        ],
        "へ": [_DummyToken("へ", "助詞", "ヘ", "エ")],
        "を": [_DummyToken("を", "助詞", "ヲ", "オ")],
    }

    def __call__(self, text):
        return self.tokens_by_text.get(text, [])


def _convert_test_romaji(kana, surface=None):
    return kana_to_romaji(kana, surface)


class ConversionCoreTests(unittest.TestCase):
    def test_ensure_custom_dict_schema_fills_missing_keys(self):
        data = ensure_custom_dict_schema({"normal_words": {"学校": ["がっこう"]}})
        self.assertIn("normal_words", data)
        self.assertIn("compound_words", data)
        self.assertIn("prefix_combinations", data)
        self.assertIn("suffix_combinations", data)

    def test_kana_to_romaji_handles_long_vowel_sokuon_and_explicit_final_override(self):
        self.assertEqual(kana_to_romaji("がっこう", "学校"), "gakkou")
        self.assertEqual(kana_to_romaji("しゅっちょう", "出張"), "shutchou")
        self.assertEqual(kana_to_romaji("すーぱー", "スーパー"), "suupaa")
        self.assertEqual(kana_to_romaji("は"), "ha")
        self.assertEqual(kana_to_romaji("はは"), "haha")
        self.assertEqual(kana_to_romaji("ははは"), "hahaha")
        self.assertEqual(kana_to_romaji("それでは"), "soredeha")

    def test_conversion_uses_morphology_and_pronunciation_for_final_particles(self):
        dictionary = ensure_custom_dict_schema({
            "normal_words": {
                "は": ["は"],
                "はは": ["はは"],
                "ははは": ["ははは"],
                "それでは": ["それでは"],
                "こんにちは": ["こんにちは"],
                "へ": ["へ"],
                "を": ["を"],
            },
        })
        expected = {
            "は": "[は] → [は] → [ハ] → [wa]",
            "はは": "[はは] → [はは] → [ハハ] → [haha]",
            "ははは": "[ははは] → [ははは] → [ハハハ] → [hahaha]",
            "それでは": "[それでは] → [それでは] → [ソレデハ] → [soredewa]",
            "こんにちは": "[こんにちは] → [こんにちは] → [コンニチハ] → [konnichiwa]",
            "へ": "[へ] → [へ] → [ヘ] → [e]",
            "を": "[を] → [を] → [ヲ] → [o]",
        }

        for text, expected_output in expected.items():
            with self.subTest(text=text):
                result = convert_text_payload(
                    text,
                    dictionary,
                    _ParticleAwareTagger(),
                    _DummyConv(),
                    True,
                    True,
                    True,
                    _convert_test_romaji,
                    conflict_detection=False,
                )
                self.assertEqual(result, expected_output)

    def test_conversion_does_not_combine_tokens_across_newline(self):
        dictionary = ensure_custom_dict_schema({
            "compound_words": {
                "こんにちは": ["こんにちは"],
            },
        })
        result = convert_text_payload(
            "こんにち\nは",
            dictionary,
            _ParticleAwareTagger(),
            _DummyConv(),
            True,
            True,
            True,
            _convert_test_romaji,
            conflict_detection=False,
        )
        self.assertEqual(
            result,
            "[こんにち] → [こんにち] → [コンニチ] → [konnichi]\n"
            "[は] → [は] → [ハ] → [wa]",
        )

    def test_format_reading_line_formats_all_selected_outputs(self):
        line = format_reading_line(
            "学校",
            ["がっこう"],
            True,
            True,
            True,
            lambda kana, surface: kana_to_romaji(kana, surface),
        )
        self.assertEqual(line, "[学校] → [がっこう] → [ガッコウ] → [gakkou]")

    def test_convert_text_payload_requires_output_mode(self):
        result = convert_text_payload(
            "学校",
            ensure_custom_dict_schema({}),
            _DummyTagger(),
            _DummyConv(),
            False,
            False,
            False,
            lambda kana, surface: kana,
        )
        self.assertEqual(result, "请选择至少一个转换方式")


if __name__ == "__main__":
    unittest.main()
