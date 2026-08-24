from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ha_client import EntityQuery, HAClient
    from home_resolver import QueryPlan


@dataclass
class CountResults:
    counts: dict[str, int] = field(default_factory=dict)
    automation_on: int = 0
    automation_off: int = 0
    automation_unknown: int = 0
    automation_unavailable: int = 0


@dataclass
class TruncatedResults:
    items: list[dict]
    total_count: int
    remaining_count: int


@dataclass
class HomeReport:
    windows_open: TruncatedResults
    doors_open: TruncatedResults
    lights_on: TruncatedResults
    automation_on: int
    automation_off: int
    automation_unknown: int
    automation_unavailable: int
    unavailable_total: int


class HomeAggregateService:
    async def execute_plan(
        self,
        ha_client: HAClient,
        plan: QueryPlan,
        max_entity_list: int,
    ) -> CountResults | HomeReport | None:
        states_snapshot = await ha_client.get_states()

        if plan.plan_type == "count_query":
            return self.build_count_results(
                plan,
                states_snapshot,
            )

        if plan.plan_type == "report":
            return self.build_home_report(
                plan,
                states_snapshot,
                max_entity_list,
            )

        return None

    def build_count_results(
        self,
        plan: QueryPlan,
        states_snapshot: list,
    ) -> CountResults:
        results = CountResults()

        for target, query in plan.queries:
            entities = self.filter_entities(
                states_snapshot,
                query,
            )

            results.counts[target] = len(entities)

            if target == "automation":
                (
                    results.automation_on,
                    results.automation_off,
                    results.automation_unknown,
                    results.automation_unavailable,
                ) = self.count_automation_states(entities)

        return results

    def build_home_report(
        self,
        plan: QueryPlan,
        states_snapshot: list,
        max_entity_list: int,
    ) -> HomeReport:
        query_map = {
            target: query
            for target, query in plan.queries
        }

        windows = self.filter_entities(
            states_snapshot,
            query_map["window"],
        )

        doors = self.filter_entities(
            states_snapshot,
            query_map["door"],
        )

        lights = self.filter_entities(
            states_snapshot,
            query_map["light"],
        )

        automations = self.filter_entities(
            states_snapshot,
            query_map["automation"],
        )

        (
            automation_on,
            automation_off,
            automation_unknown,
            automation_unavailable,
        ) = self.count_automation_states(automations)

        unavailable_total = sum(
            1
            for item in states_snapshot
            if str(item.get("state", "unknown")).lower()
            == "unavailable"
        )

        return HomeReport(
            windows_open=self.truncate_results(
                windows,
                max_entity_list,
            ),
            doors_open=self.truncate_results(
                doors,
                max_entity_list,
            ),
            lights_on=self.truncate_results(
                lights,
                max_entity_list,
            ),
            automation_on=automation_on,
            automation_off=automation_off,
            automation_unknown=automation_unknown,
            automation_unavailable=automation_unavailable,
            unavailable_total=unavailable_total,
        )

    def truncate_results(
        self,
        items: list[dict],
        max_entity_list: int,
    ) -> TruncatedResults:
        max_items = max_entity_list

        if max_items <= 0:
            max_items = 10

        total_count = len(items)

        if total_count <= max_items:
            return TruncatedResults(
                items=list(items),
                total_count=total_count,
                remaining_count=0,
            )

        return TruncatedResults(
            items=list(items[:max_items]),
            total_count=total_count,
            remaining_count=total_count - max_items,
        )

    def count_automation_states(
        self,
        entities: list[dict],
    ) -> tuple[int, int, int, int]:
        on_count = 0
        off_count = 0
        unknown_count = 0
        unavailable_count = 0

        for item in entities:
            state = str(item.get("state", "unknown")).lower()

            if state == "on":
                on_count += 1
            elif state == "off":
                off_count += 1
            elif state == "unavailable":
                unavailable_count += 1
            else:
                unknown_count += 1

        return (
            on_count,
            off_count,
            unknown_count,
            unavailable_count,
        )

    def filter_entities(
        self,
        states_snapshot: list,
        query: EntityQuery,
    ) -> list[dict]:
        results = []

        expected_classes = {
            value.lower()
            for value in query.device_classes
        }

        expected_states = {
            value.lower()
            for value in query.states
        }

        expected_terms = [
            value.lower()
            for value in query.name_terms
        ]

        for item in states_snapshot:
            entity_id = item.get("entity_id", "")

            if "." in entity_id:
                domain = entity_id.split(".", 1)[0]
            else:
                domain = ""

            attributes = item.get("attributes", {})

            device_class = str(
                attributes.get("device_class", "")
            ).lower()

            state = str(
                item.get("state", "unknown")
            ).lower()

            name = str(
                attributes.get("friendly_name", entity_id)
            )

            if query.domain and domain != query.domain:
                continue

            if (
                expected_classes
                and device_class not in expected_classes
            ):
                continue

            if expected_states and state not in expected_states:
                continue

            if (
                expected_terms
                and not any(
                    term in name.lower()
                    for term in expected_terms
                )
            ):
                continue

            results.append({
                "entity_id": entity_id,
                "name": name,
                "domain": domain,
                "device_class": device_class or None,
                "state": state,
            })

        return results


