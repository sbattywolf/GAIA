import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from home_intents import parse_home_intent
from home_resolver import (
    QueryPlan,
    resolve_intent_to_plan,
    resolve_intent_to_query,
)


class HomeResolverM2Tests(unittest.TestCase):
    def test_resolve_state_query_contract_is_unchanged(self):
        intent = parse_home_intent(
            "quali luci sono accese?",
        )

        query = resolve_intent_to_query(intent)

        self.assertIsNotNone(query)
        self.assertEqual(query.domain, "light")
        self.assertEqual(query.states, ["on"])

    def test_resolve_plan_returns_none_for_state_query(self):
        intent = parse_home_intent(
            "quali porte sono aperte?",
        )

        self.assertIsNone(resolve_intent_to_plan(intent))

    def test_resolve_count_plan_for_multi_category(self):
        intent = parse_home_intent(
            "quante luci, switch, porte e finestre ho?",
        )

        plan = resolve_intent_to_plan(intent)

        self.assertIsInstance(plan, QueryPlan)
        self.assertEqual(plan.plan_type, "count_query")
        self.assertEqual(
            [target for target, _ in plan.queries],
            ["window", "door", "light", "switch"],
        )

    def test_resolve_report_plan(self):
        intent = parse_home_intent(
            "fammi un report dello stato della casa",
        )

        plan = resolve_intent_to_plan(intent)

        self.assertIsInstance(plan, QueryPlan)
        self.assertEqual(plan.plan_type, "report")
        self.assertEqual(
            [target for target, _ in plan.queries],
            ["window", "door", "light", "automation"],
        )


if __name__ == "__main__":
    unittest.main()

