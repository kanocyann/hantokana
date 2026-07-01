import unittest

from hantokana_app.dict_migration_core import build_official_dict_sync_plan, resolve_official_dict_sync


class DictMigrationCoreTests(unittest.TestCase):
    def test_build_official_dict_sync_plan_skips_shared_items(self):
        state_snapshot = {
            "sha256": "old",
            "dict": {
                "normal_words": {"学校": ["がっこう"]},
                "compound_words": {},
                "prefix_combinations": {},
                "suffix_combinations": {},
            },
        }
        local_dict = {
            "normal_words": {"学校": ["がっこう"], "出張": ["しゅっちょう"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }
        official_dict = {
            "normal_words": {"学校": ["がっこう"], "出張": ["しゅっちょう2"]},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {},
        }

        plan = build_official_dict_sync_plan(state_snapshot, local_dict, official_dict, "ask")

        self.assertEqual(plan["summary"]["total"], 1)
        self.assertEqual(plan["items"][0]["word"], "出張")
        self.assertEqual(plan["items"][0]["change_type"], "conflict_new")

    def test_resolve_official_dict_sync_keeps_default_action(self):
        plan = {
            "local_dict": {
                "normal_words": {"学校": ["がっこう"]},
                "compound_words": {},
                "prefix_combinations": {},
                "suffix_combinations": {},
            },
            "items": [
                {
                    "group": "normal_words",
                    "word": "学校",
                    "local": ["がっこう"],
                    "official": ["がっこう2"],
                    "default_action": "use_official",
                    "recommended_action": "merge",
                }
            ],
        }

        merged = resolve_official_dict_sync(plan)
        self.assertEqual(merged["normal_words"]["学校"], ["がっこう2"])


if __name__ == "__main__":
    unittest.main()
