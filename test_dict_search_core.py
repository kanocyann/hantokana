import unittest

from hantokana_app.dict_search_core import calculate_total_pages, entry_at_page_row, filter_entries, get_page_entries


class DictSearchCoreTests(unittest.TestCase):
    def setUp(self):
        self.entries = [
            {"word": "学校", "readings": "がっこう", "type": "普通词"},
            {"word": "出張", "readings": "しゅっちょう", "type": "复合词"},
            {"word": "まで", "readings": "今, 夢", "type": "前缀组合"},
        ]

    def test_filter_entries_uses_type_and_keywords(self):
        self.assertEqual(filter_entries(self.entries, "复合词", "しゅっ"), [self.entries[1]])
        self.assertEqual(filter_entries(self.entries, "全部", "学校 がっ"), [self.entries[0]])

    def test_calculate_total_pages_clamps_to_at_least_one(self):
        self.assertEqual(calculate_total_pages(0, 50), 1)
        self.assertEqual(calculate_total_pages(101, 50), 3)
        self.assertEqual(calculate_total_pages(2, 0), 2)

    def test_get_page_entries_returns_start_index_and_entries(self):
        start_idx, page_entries = get_page_entries(self.entries, 2, 2)

        self.assertEqual(start_idx, 2)
        self.assertEqual(page_entries, [self.entries[2]])

    def test_entry_at_page_row_maps_visible_row_to_filtered_entry(self):
        self.assertEqual(entry_at_page_row(self.entries, 2, 2, 0), self.entries[2])
        self.assertIsNone(entry_at_page_row(self.entries, 2, 2, 1))


if __name__ == "__main__":
    unittest.main()
