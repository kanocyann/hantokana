import json
import tempfile
import unittest
from pathlib import Path

from hantokana_app.storage_core import import_dict_file, load_custom_dict, merge_dict_payload, resource_path


class StorageCoreTests(unittest.TestCase):
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

    def test_load_custom_dict_initializes_from_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            dict_path = tmpdir / "custom_dict.json"
            resource_path_file = tmpdir / "resource.json"
            resource_payload = {"normal_words": {"学校": ["がっこう"]}}
            resource_path_file.write_text(json.dumps(resource_payload, ensure_ascii=False), encoding="utf-8")

            data, loaded_path = load_custom_dict(str(dict_path), str(resource_path_file))

            self.assertEqual(loaded_path, str(dict_path))
            self.assertTrue(dict_path.exists())
            self.assertEqual(data["normal_words"]["学校"], ["がっこう"])

    def test_import_dict_file_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            invalid_path = tmpdir / "broken.json"
            invalid_path.write_text("{", encoding="utf-8")

            with self.assertRaises(ValueError):
                import_dict_file({}, str(invalid_path))


if __name__ == "__main__":
    unittest.main()
