import json
import tempfile
import unittest
from pathlib import Path

from hantokana_app.storage_core import (
    import_dict_file,
    load_effective_dict,
    load_custom_dict,
    load_official_dict,
    merge_dict_payload,
    resource_path,
    sync_official_dict_to_appdata,
    save_effective_dict,
)
from hantokana_app.app_config import (
    APP_VERSION,
    CONFIG_SCHEMA_VERSION,
    default_app_config,
    merge_app_config,
    normalize_app_config,
)


class StorageCoreTests(unittest.TestCase):
    def test_normalize_app_config_adds_defaults_and_metadata(self):
        normalized = normalize_app_config({"close_action": "exit"})

        self.assertEqual(normalized["close_action"], "exit")
        self.assertEqual(normalized["entries_per_page"], 20)
        self.assertEqual(normalized["enable_conflict_detection"], False)
        self.assertEqual(normalized["_schema_version"], CONFIG_SCHEMA_VERSION)
        self.assertEqual(normalized["_app_version"], APP_VERSION)

    def test_normalize_app_config_drops_unknown_fields_and_stale_meta(self):
        normalized = normalize_app_config({
            "close_action": "exit",
            "legacy_field": "old",
            "official_dict_merge_policy": "ask",
            "_schema_version": 1,
            "_custom_meta": "keep me",
        })

        self.assertEqual(normalized["close_action"], "exit")
        self.assertNotIn("legacy_field", normalized)
        self.assertNotIn("official_dict_merge_policy", normalized)
        self.assertNotIn("_custom_meta", normalized)
        self.assertEqual(normalized["_schema_version"], CONFIG_SCHEMA_VERSION)

    def test_merge_app_config_preserves_user_values(self):
        existing = default_app_config()
        existing["enable_conflict_detection"] = False
        merged = merge_app_config(existing, {"entries_per_page": 50})

        self.assertEqual(merged["enable_conflict_detection"], False)
        self.assertEqual(merged["entries_per_page"], 50)

    def test_merge_app_config_ignores_unknown_update_fields(self):
        merged = merge_app_config({"entries_per_page": 20}, {
            "entries_per_page": 100,
            "future_or_removed_field": True,
        })

        self.assertEqual(merged["entries_per_page"], 100)
        self.assertNotIn("future_or_removed_field", merged)

    def test_merge_dict_payload_preserves_order_and_deduplicates(self):
        base = {
            "normal_words": {"学校": ["がっこう"]},
            "compound_words": {},
            "prefix_combinations": {"お": ["名詞", "名詞"]},
            "suffix_combinations": {"って": ["助詞"]},
        }
        incoming = {
            "normal_words": {"出張": ["しゅっちょう"]},
            "compound_words": {"今日": ["きょう"]},
            "prefix_combinations": {"お": ["名詞", "動詞"]},
            "suffix_combinations": {"って": ["助詞", "終助詞"]},
        }

        merged = merge_dict_payload(base, incoming)

        self.assertEqual(merged["normal_words"]["学校"], ["がっこう"])
        self.assertEqual(merged["normal_words"]["出張"], ["しゅっちょう"])
        self.assertEqual(merged["compound_words"]["今日"], ["きょう"])
        self.assertEqual(merged["prefix_combinations"]["お"], ["名詞", "動詞"])
        self.assertEqual(merged["suffix_combinations"]["って"], ["助詞", "終助詞"])

    def test_merge_dict_payload_preserves_delete_markers_for_combinations(self):
        base = {
            "normal_words": {},
            "compound_words": {},
            "prefix_combinations": {"お": ["名詞"]},
            "suffix_combinations": {"それ": ["で"]},
        }
        incoming = {
            "normal_words": {},
            "compound_words": {},
            "prefix_combinations": {"お": []},
            "suffix_combinations": {"それ": []},
        }

        merged = merge_dict_payload(base, incoming)

        self.assertEqual(merged["prefix_combinations"]["お"], [])
        self.assertEqual(merged["suffix_combinations"]["それ"], [])

    def test_load_custom_dict_initializes_empty_user_dict(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            dict_path = tmpdir / "custom_dict.json"
            resource_path_file = tmpdir / "resource.json"
            resource_payload = {"normal_words": {"学校": ["がっこう"]}}
            resource_path_file.write_text(json.dumps(resource_payload, ensure_ascii=False), encoding="utf-8")

            data, loaded_path = load_custom_dict(str(dict_path), str(resource_path_file))

            self.assertEqual(loaded_path, str(dict_path))
            self.assertTrue(dict_path.exists())
            self.assertEqual(data["normal_words"], {})

    def test_sync_official_dict_to_appdata_overwrites_official_copy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_path = tmpdir / "packaged.json"
            target_path = tmpdir / "official_dict.json"
            source_path.write_text(
                json.dumps({"normal_words": {"学校": ["がっこう"]}}, ensure_ascii=False),
                encoding="utf-8",
            )
            target_path.write_text(
                json.dumps({"normal_words": {"古い": ["ふるい"]}}, ensure_ascii=False),
                encoding="utf-8",
            )

            data, synced_path = sync_official_dict_to_appdata(str(source_path), str(target_path))

            self.assertEqual(synced_path, str(target_path))
            self.assertEqual(data["normal_words"]["学校"], ["がっこう"])
            self.assertEqual(load_official_dict(str(target_path))["normal_words"]["学校"], ["がっこう"])

    def test_effective_dict_cache_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            cache_path = tmpdir / "effective_dict.json"
            payload = {
                "normal_words": {"今日": ["こんにち"]},
                "compound_words": {},
                "prefix_combinations": {},
                "suffix_combinations": {},
            }

            save_effective_dict(str(cache_path), payload)
            loaded = load_effective_dict(str(cache_path))

            self.assertEqual(loaded["normal_words"]["今日"], ["こんにち"])

    def test_import_dict_file_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            invalid_path = tmpdir / "broken.json"
            invalid_path.write_text("{", encoding="utf-8")

            with self.assertRaises(ValueError):
                import_dict_file({}, str(invalid_path))


if __name__ == "__main__":
    unittest.main()
