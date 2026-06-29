import unittest

from hantokana_app.dict_edit_core import (
    delete_dict_entries,
    format_entry_text,
    iter_edit_entries,
    parse_entry_display_text,
    set_dict_entry,
    split_entry_values,
)


class DictEditCoreTests(unittest.TestCase):
    def test_split_entry_values_accepts_common_separators(self):
        self.assertEqual(split_entry_values("がっこう，がくこう、 学校"), ["がっこう", "がくこう", "学校"])

    def test_set_dict_entry_creates_bucket_and_reports_existing(self):
        custom_dict = {}

        existed = set_dict_entry(custom_dict, "normal_words", "学校", ["がっこう"])
        self.assertFalse(existed)
        self.assertEqual(custom_dict["normal_words"]["学校"], ["がっこう"])

        existed = set_dict_entry(custom_dict, "normal_words", "学校", ["がくこう"])
        self.assertTrue(existed)
        self.assertEqual(custom_dict["normal_words"]["学校"], ["がくこう"])

    def test_delete_dict_entries_returns_deleted_count(self):
        custom_dict = {"normal_words": {"学校": ["がっこう"], "出張": ["しゅっちょう"]}}

        deleted = delete_dict_entries(custom_dict, "normal_words", ["学校", "missing"])

        self.assertEqual(deleted, 1)
        self.assertNotIn("学校", custom_dict["normal_words"])
        self.assertIn("出張", custom_dict["normal_words"])

    def test_iter_edit_entries_sorts_by_word(self):
        custom_dict = {"normal_words": {"出張": ["しゅっちょう"], "学校": ["がっこう"]}}

        entries = list(iter_edit_entries(custom_dict, "normal_words"))

        self.assertEqual(entries, [("出張", ["しゅっちょう"]), ("学校", ["がっこう"])])

    def test_format_and_parse_entry_text(self):
        text = format_entry_text("学校", ["がっこう", "がくこう"])

        self.assertEqual(text, "学校 → がっこう, がくこう")
        self.assertEqual(parse_entry_display_text(text), ("学校", "がっこう, がくこう"))


if __name__ == "__main__":
    unittest.main()
