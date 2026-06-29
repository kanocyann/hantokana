import unittest

from hantokana_app.conversion_core import ensure_custom_dict_schema, format_reading_line, kana_to_romaji
from hantokana_app.conversion_service import convert_text_payload


class _DummyTagger:
    def __call__(self, text):
        return []


class _DummyConv:
    def convert(self, word):
        return [{"hira": word}]


class ConversionCoreTests(unittest.TestCase):
    def test_ensure_custom_dict_schema_fills_missing_keys(self):
        data = ensure_custom_dict_schema({"normal_words": {"学校": ["がっこう"]}})
        self.assertIn("normal_words", data)
        self.assertIn("compound_words", data)
        self.assertIn("prefix_combinations", data)
        self.assertIn("suffix_combinations", data)

    def test_kana_to_romaji_handles_long_vowel_sokuon_and_particles(self):
        self.assertEqual(kana_to_romaji("がっこう", "学校"), "gakkou")
        self.assertEqual(kana_to_romaji("しゅっちょう", "出張"), "shutchou")
        self.assertEqual(kana_to_romaji("すーぱー", "スーパー"), "suupaa")
        self.assertEqual(kana_to_romaji("それでは", "それでは"), "soredewa")
        self.assertEqual(kana_to_romaji("こんにちは", "今日は"), "konnichiwa")
        self.assertEqual(kana_to_romaji("あしたは", "明日は"), "ashitawa")

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
