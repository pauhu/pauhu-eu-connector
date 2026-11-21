"""Black-box check of the published files: valid JSON, unique ids, required fields, policy shape. Offline."""
import json, os, unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ("dcat:keyword", "dct:language", "dct:description", "dct:publisher", "dcat:version", "accessUrl")


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return json.load(f)


class Files(unittest.TestCase):
    def test_entries(self):
        entries = load("entries.json")
        self.assertEqual(len(entries), 17)
        ids = [e["@id"] for e in entries]
        self.assertEqual(len(set(ids)), len(ids))
        for e in entries:
            self.assertEqual(e["@type"], "Asset")
            for k in REQUIRED:
                self.assertIn(k, e["properties"], (e["@id"], k))

    def test_policies(self):
        policies = load("policies.json")
        self.assertEqual(len(policies), 10)
        for p in policies:
            self.assertEqual(p["policy"]["@type"], "odrl:Set")
            self.assertIn("odrl:permission", p["policy"])


if __name__ == "__main__":
    unittest.main()
