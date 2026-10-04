import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_registry import validate  # noqa: E402


class RegistryValidationTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))

    def test_current_registry_is_valid(self):
        self.assertEqual(validate(self.registry), [])

    def test_missing_control_is_rejected(self):
        broken = dict(self.registry)
        broken["abstention_controls"] = broken["abstention_controls"][:-1]
        self.assertIn("exactly 6 abstention controls are required", validate(broken))

    def test_non_abstention_control_is_rejected(self):
        broken = json.loads(json.dumps(self.registry))
        broken["abstention_controls"][0]["expected_decision"] = "EDIT"
        self.assertIn("all control cases must require ABSTAIN", validate(broken))
