import unittest

from hantokana_app.dict_view_core import (
    entry_matches_filters,
    get_dict_type_meta,
    highlight_text,
    iter_custom_dict_entries,
    split_search_keywords,
)


class DictViewCoreTests(unittest.TestCase):
    def test_get_dict_type_meta_returns_expected_labels(self):
        meta = get_dict_type_meta("prefix_combinations")
        self.assertEqual(meta["dialog_title"], "常见前缀组合")
        self.assertEqual(meta["display_name"], "前缀组合")

    def test_iter_custom_dict_entries_formats_and_orders_entries(self):
        custom_dict = {
            "compound_words": {"出張": ["しゅっちょう"]},
            "normal_words": {"学校": ["がっこう", "がくこう"]},
            "prefix_combinations": {"お": ["名詞"]},
            "suffix_combinations": {},
        }

        entries = list(iter_custom_dict_entries(custom_dict))

        self.assertEqual([entry["word"] for entry in entries], ["学校", "出張", "お"])
        self.assertEqual(entries[0]["readings"], "がっこう, がくこう")
        self.assertEqual(entries[2]["type"], "前缀组合")

    def test_split_search_keywords_normalizes_input(self):
        self.assertEqual(split_search_keywords(" 学校  出張 "), ["学校", "出張"])

    def test_entry_matches_filters_checks_type_and_keywords(self):
        entry = {"word": "学校", "readings": "がっこう", "type": "普通词"}

        self.assertTrue(entry_matches_filters(entry, "普通词", ["学校"]))
        self.assertFalse(entry_matches_filters(entry, "复合词", ["学校"]))
        self.assertFalse(entry_matches_filters(entry, "普通词", ["出張"]))

    def test_highlight_text_wraps_all_matches(self):
        highlighted = highlight_text("学校A学校", ["学校"])
        self.assertEqual(
            highlighted,
            '<span style="background-color: #FFFF00;">学校</span>A'
            '<span style="background-color: #FFFF00;">学校</span>',
        )


if __name__ == "__main__":
    unittest.main()
