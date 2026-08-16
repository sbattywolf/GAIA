import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from home_intents import (
    HomeIntent,
    normalize_device_targets,
    parse_home_intent,
)


class HomeIntentM2Tests(unittest.TestCase):
    def test_count_single_target_automation(self):
        intent = parse_home_intent(
            "quante automazioni ci sono?",
        )

        self.assertEqual(intent.intent_type, "count_query")
        self.assertEqual(
            normalize_device_targets(intent),
            ["automation"],
        )

    def test_count_multi_category(self):
        intent = parse_home_intent(
            "quante luci, switch, porte e finestre ho?",
        )

        self.assertEqual(intent.intent_type, "count_query")
        self.assertEqual(
            normalize_device_targets(intent),
            ["window", "door", "light", "switch"],
        )

    def test_report_intent(self):
        intent = parse_home_intent(
            "fammi un report dello stato della casa",
        )

        self.assertEqual(intent.intent_type, "report")
        self.assertGreaterEqual(intent.confidence, 0.90)

    def test_accesse_typo_maps_to_on(self):
        intent = parse_home_intent(
            "ci sono luci accesse?",
        )

        self.assertEqual(intent.intent_type, "state_query")
        self.assertEqual(intent.device_kind, "light")
        self.assertEqual(intent.desired_state, "on")

    def test_normalize_merges_dedups_and_orders(self):
        intent = HomeIntent(
            intent_type="count_query",
            device_kind="switch",
            device_kinds=["light", "switch", "door"],
        )

        self.assertEqual(
            normalize_device_targets(intent),
            ["door", "light", "switch"],
        )

    def test_normalize_ignores_unknown_targets(self):
        intent = HomeIntent(
            intent_type="count_query",
            device_kind="light",
            device_kinds=["unknown_kind", "window"],
        )

        self.assertEqual(
            normalize_device_targets(intent),
            ["window", "light"],
        )


if __name__ == "__main__":
    unittest.main()

