from __future__ import annotations

from dataclasses import dataclass, field

from ha_client import EntityQuery

from home_intents import HomeIntent, normalize_device_targets


DEVICE_KIND_MAPPING = {
    "window": {
        "domain": "binary_sensor",
        "device_classes": [
            "window",
            "opening",
        ],
    },
    "door": {
        "domain": "binary_sensor",
        "device_classes": [
            "door",
            "opening",
        ],
    },
    "light": {
        "domain": "light",
        "device_classes": [],
    },
    "switch": {
        "domain": "switch",
        "device_classes": [],
    },
    "automation": {
        "domain": "automation",
        "device_classes": [],
    },
}


@dataclass
class QueryPlan:
    plan_type: str
    queries: list[tuple[str, EntityQuery]]


def resolve_intent_to_query(
    intent: HomeIntent,
) -> EntityQuery | None:

    mapping = DEVICE_KIND_MAPPING.get(
        intent.device_kind
    )

    if not mapping:
        return None

    states = []

    if intent.desired_state:
        states.append(
            intent.desired_state
        )

    return EntityQuery(
        domain=mapping["domain"],
        device_classes=list(
            mapping["device_classes"]
        ),
        states=states,
        name_terms=[],
    )


def resolve_intent_to_plan(
    intent: HomeIntent,
) -> QueryPlan | None:
    if intent.intent_type == "count_query":
        targets = normalize_device_targets(intent)

        if not targets:
            return None

        queries = []

        for target in targets:
            mapping = DEVICE_KIND_MAPPING.get(target)

            if not mapping:
                continue

            queries.append((
                target,
                EntityQuery(
                    domain=mapping["domain"],
                    device_classes=list(
                        mapping["device_classes"]
                    ),
                    states=[],
                    name_terms=[],
                ),
            ))

        if not queries:
            return None

        return QueryPlan(
            plan_type="count_query",
            queries=queries,
        )

    if intent.intent_type == "report":
        queries = [
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
        ]

        return QueryPlan(
            plan_type="report",
            queries=queries,
        )

    return None
