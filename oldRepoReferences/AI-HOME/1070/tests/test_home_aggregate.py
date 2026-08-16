import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock


APP_DIR = Path(__file__).resolve().parents[1] / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from home_aggregate import HomeAggregateService
from home_intents import parse_home_intent
from home_resolver import (
    EntityQuery,
    QueryPlan,
    resolve_intent_to_plan,
)


def _entity(
    entity_id,
    state,
    device_class=None,
    name=None,
):
    attributes = {}

    if device_class:
        attributes["device_class"] = device_class

    attributes["friendly_name"] = name or entity_id

    return {
        "entity_id": entity_id,
        "state": state,
        "attributes": attributes,
    }


def _automation_entities():
    entities = []

    for index in range(28):
        entities.append(
            _entity(
                f"automation.auto_on_{index}",
                "on",
                name=f"Auto ON {index}",
            )
        )

    for index in range(6):
        entities.append(
            _entity(
                f"automation.auto_off_{index}",
                "off",
                name=f"Auto OFF {index}",
            )
        )

    entities.append(
        _entity(
            "automation.auto_unavailable",
            "unavailable",
            name="Auto Unavailable",
        )
    )

    entities.append(
        _entity(
            "automation.auto_unknown",
            "unknown",
            name="Auto Unknown",
        )
    )

    return entities


class FakeHAClient:
    def __init__(self, snapshot):
        self.get_states = AsyncMock(return_value=snapshot)


class HomeAggregateServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = HomeAggregateService()

    async def test_count_single_automation(self):
        snapshot = _automation_entities()
        ha_client = FakeHAClient(snapshot)

        plan = resolve_intent_to_plan(
            parse_home_intent("quante automazioni ci sono?"),
        )

        result = await self.service.execute_plan(
            ha_client,
            plan,
            10,
        )

        self.assertEqual(ha_client.get_states.await_count, 1)
        self.assertEqual(result.counts["automation"], 36)
        self.assertEqual(result.automation_on, 28)
        self.assertEqual(result.automation_off, 6)
        self.assertEqual(result.automation_unknown, 1)
        self.assertEqual(result.automation_unavailable, 1)

    async def test_count_multi_category(self):
        snapshot = [
            _entity("binary_sensor.finestra_1", "on", "window", "Finestra 1"),
            _entity("binary_sensor.finestra_2", "off", "window", "Finestra 2"),
            _entity("binary_sensor.porta_1", "off", "door", "Porta 1"),
            _entity("light.luce_1", "on", name="Luce 1"),
            _entity("light.luce_2", "off", name="Luce 2"),
            _entity("switch.switch_1", "on", name="Switch 1"),
        ]
        ha_client = FakeHAClient(snapshot)

        plan = resolve_intent_to_plan(
            parse_home_intent(
                "quante luci, switch, porte e finestre ho?",
            )
        )

        result = await self.service.execute_plan(
            ha_client,
            plan,
            10,
        )

        self.assertEqual(ha_client.get_states.await_count, 1)
        self.assertEqual(result.counts["window"], 2)
        self.assertEqual(result.counts["door"], 1)
        self.assertEqual(result.counts["light"], 2)
        self.assertEqual(result.counts["switch"], 1)

    async def test_report_minimum_payload(self):
        snapshot = [
            _entity("binary_sensor.finestra_1", "on", "window", "Finestra 1"),
            _entity("binary_sensor.porta_1", "off", "door", "Porta 1"),
            _entity("light.luce_1", "on", name="Luce 1"),
            _entity("light.luce_2", "on", name="Luce 2"),
            _entity("light.luce_3", "on", name="Luce 3"),
            _entity("light.luce_4", "on", name="Luce 4"),
            _entity("sensor.generico", "unavailable", name="Sensore X"),
        ] + _automation_entities()

        ha_client = FakeHAClient(snapshot)
        plan = resolve_intent_to_plan(
            parse_home_intent(
                "fammi un report dello stato della casa",
            )
        )

        report = await self.service.execute_plan(
            ha_client,
            plan,
            2,
        )

        self.assertEqual(ha_client.get_states.await_count, 1)

        self.assertEqual(report.windows_open.total_count, 1)
        self.assertEqual(report.windows_open.remaining_count, 0)

        self.assertEqual(report.doors_open.total_count, 0)
        self.assertEqual(report.doors_open.remaining_count, 0)

        self.assertEqual(report.lights_on.total_count, 4)
        self.assertEqual(len(report.lights_on.items), 2)
        self.assertEqual(report.lights_on.remaining_count, 2)

        self.assertEqual(report.automation_on, 28)
        self.assertEqual(report.automation_off, 6)
        self.assertEqual(report.automation_unknown, 1)
        self.assertEqual(report.automation_unavailable, 1)

        self.assertEqual(report.unavailable_total, 2)

    def test_truncate_results_first_n_plus_remaining(self):
        items = [
            {"name": "Uno"},
            {"name": "Due"},
            {"name": "Tre"},
            {"name": "Quattro"},
        ]

        truncated = self.service.truncate_results(
            items,
            2,
        )

        self.assertEqual(truncated.total_count, 4)
        self.assertEqual(len(truncated.items), 2)
        self.assertEqual(truncated.remaining_count, 2)

    def test_filter_entities_matches_query(self):
        snapshot = [
            _entity("binary_sensor.finestra_1", "on", "window", "Finestra 1"),
            _entity("binary_sensor.porta_1", "on", "door", "Porta 1"),
            _entity("binary_sensor.finestra_2", "off", "window", "Finestra 2"),
        ]

        query = EntityQuery(
            domain="binary_sensor",
            device_classes=["window"],
            states=["on"],
            name_terms=[],
        )

        results = self.service.filter_entities(
            snapshot,
            query,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Finestra 1")

    async def test_count_and_report_use_single_snapshot_each(self):
        snapshot = _automation_entities()
        ha_client = FakeHAClient(snapshot)

        count_plan = QueryPlan(
            plan_type="count_query",
            queries=[
                (
                    "automation",
                    EntityQuery(
                        domain="automation",
                        device_classes=[],
                        states=[],
                        name_terms=[],
                    ),
                )
            ],
        )

        report_plan = QueryPlan(
            plan_type="report",
            queries=[
                (
                    "window",
                    EntityQuery(
                        domain="binary_sensor",
                        device_classes=["window", "opening"],
                        states=["on"],
                        name_terms=[],
                    ),
                ),
                (
                    "door",
                    EntityQuery(
                        domain="binary_sensor",
                        device_classes=["door", "opening"],
                        states=["on"],
                        name_terms=[],
                    ),
                ),
                (
                    "light",
                    EntityQuery(
                        domain="light",
                        device_classes=[],
                        states=["on"],
                        name_terms=[],
                    ),
                ),
                (
                    "automation",
                    EntityQuery(
                        domain="automation",
                        device_classes=[],
                        states=[],
                        name_terms=[],
                    ),
                ),
            ],
        )

        await self.service.execute_plan(
            ha_client,
            count_plan,
            10,
        )

        self.assertEqual(ha_client.get_states.await_count, 1)

        await self.service.execute_plan(
            ha_client,
            report_plan,
            10,
        )

        self.assertEqual(ha_client.get_states.await_count, 2)


if __name__ == "__main__":
    unittest.main()


