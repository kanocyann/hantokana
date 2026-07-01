import unittest

from hantokana_app.dict_migration_core import (
    build_effective_dict_cache,
    dict_entry_source,
    is_deleted_marker,
    merge_official_and_custom_dicts,
    prune_redundant_custom_entries,
    source_label,
    SOURCE_CUSTOM,
    SOURCE_DELETED,
    SOURCE_OFFICIAL,
    SOURCE_OVERRIDE,
)


class DictMigrationCoreTests(unittest.TestCase):
    def test_merge_official_and_custom_uses_official_base_and_user_delta(self):
        official_dict = {
            "normal_words": {"今日": ["きょう"], "学校": ["がっこう"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {"今日": ["こんにち"], "私物": ["しぶつ"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        merged = merge_official_and_custom_dicts(official_dict, custom_dict)

        self.assertEqual(merged["normal_words"]["今日"], ["こんにち"])
        self.assertEqual(merged["normal_words"]["学校"], ["がっこう"])
        self.assertEqual(merged["normal_words"]["私物"], ["しぶつ"])

    def test_empty_custom_value_deletes_official_entry_from_effective_dict(self):
        official_dict = {
            "normal_words": {"今日": ["きょう"], "学校": ["がっこう"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {"今日": []},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        merged = merge_official_and_custom_dicts(official_dict, custom_dict)

        self.assertNotIn("今日", merged["normal_words"])
        self.assertEqual(merged["normal_words"]["学校"], ["がっこう"])
        self.assertTrue(is_deleted_marker([]))

    def test_build_effective_dict_cache_uses_user_overrides(self):
        official_dict = {
            "normal_words": {"今日": ["きょう"], "学校": ["がっこう"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {"今日": ["こんにち"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        effective = build_effective_dict_cache(official_dict, custom_dict)

        self.assertEqual(effective["normal_words"]["今日"], ["こんにち"])
        self.assertEqual(effective["normal_words"]["学校"], ["がっこう"])

    def test_dict_entry_source_distinguishes_official_custom_override_and_deleted(self):
        official_dict = {
            "normal_words": {"今日": ["きょう"], "学校": ["がっこう"], "削除": ["さくじょ"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {"今日": ["こんにち"], "私物": ["しぶつ"], "削除": []},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        self.assertEqual(dict_entry_source(official_dict, custom_dict, "normal_words", "学校"), SOURCE_OFFICIAL)
        self.assertEqual(dict_entry_source(official_dict, custom_dict, "normal_words", "私物"), SOURCE_CUSTOM)
        self.assertEqual(dict_entry_source(official_dict, custom_dict, "normal_words", "今日"), SOURCE_OVERRIDE)
        self.assertEqual(dict_entry_source(official_dict, custom_dict, "normal_words", "削除"), SOURCE_DELETED)
        self.assertEqual(source_label(SOURCE_OVERRIDE), "已修改")
        self.assertEqual(source_label(SOURCE_DELETED), "已删除")

    def test_deleted_marker_without_official_entry_is_still_visible_as_deleted(self):
        official_dict = {
            "normal_words": {},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {"私物": []},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        self.assertEqual(dict_entry_source(official_dict, custom_dict, "normal_words", "私物"), SOURCE_DELETED)
        self.assertNotIn("私物", merge_official_and_custom_dicts(official_dict, custom_dict)["normal_words"])

    def test_prune_redundant_custom_entries_keeps_only_user_delta(self):
        official_dict = {
            "normal_words": {"学校": ["がっこう"], "今日": ["きょう"], "削除": ["さくじょ"]},
            "compound_words": {},
            "prefix_combinations": {"お": ["名詞"]},
            "suffix_combinations": {},
        }
        custom_dict = {
            "normal_words": {
                "学校": ["がっこう"],
                "今日": ["こんにち"],
                "私物": ["しぶつ"],
                "削除": [],
                "古い私物": [],
            },
            "compound_words": {},
            "prefix_combinations": {"お": ["名詞"]},
            "suffix_combinations": {},
        }

        pruned, changed = prune_redundant_custom_entries(official_dict, custom_dict)

        self.assertTrue(changed)
        self.assertNotIn("学校", pruned["normal_words"])
        self.assertNotIn("お", pruned["prefix_combinations"])
        self.assertEqual(pruned["normal_words"]["今日"], ["こんにち"])
        self.assertEqual(pruned["normal_words"]["私物"], ["しぶつ"])
        self.assertEqual(pruned["normal_words"]["削除"], [])
        self.assertEqual(pruned["normal_words"]["古い私物"], [])


if __name__ == "__main__":
    unittest.main()
