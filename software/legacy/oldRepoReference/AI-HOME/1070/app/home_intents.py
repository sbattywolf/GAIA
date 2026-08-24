from __future__ import annotations

from dataclasses import dataclass, field


TARGET_ORDER = (
    "window",
    "door",
    "light",
    "switch",
    "automation",
)


@dataclass
class HomeIntent:
    intent_type: str
    device_kind: str | None = None
    device_kinds: list[str] = field(default_factory=list)
    desired_state: str | None = None
    area: str | None = None
    action: str | None = None
    requires_confirmation: bool = False
    confidence: float = 0.0


def normalize_device_targets(
    intent: HomeIntent,
) -> list[str]:
    requested = []

    if intent.device_kind:
        requested.append(intent.device_kind)

    requested.extend(intent.device_kinds)

    requested_set = {
        value
        for value in requested
        if value in TARGET_ORDER
    }

    return [
        value
        for value in TARGET_ORDER
        if value in requested_set
    ]


def _extract_count_targets(lowered: str) -> list[str]:
    targets = []

    if "finestr" in lowered:
        targets.append("window")

    if "port" in lowered:
        targets.append("door")

    if "luce" in lowered or "luci" in lowered:
        targets.append("light")

    if "switch" in lowered or "interruttor" in lowered:
        targets.append("switch")

    if "automaz" in lowered:
        targets.append("automation")

    return targets


def parse_home_intent(text: str) -> HomeIntent:
    lowered = text.lower().strip()

    if (
        "stato della casa" in lowered
        or "stato casa" in lowered
        or (
            "report" in lowered
            and "casa" in lowered
        )
    ):
        return HomeIntent(
            intent_type="report",
            confidence=0.95,
        )

    if "quant" in lowered:
        count_targets = _extract_count_targets(lowered)

        if count_targets:
            normalized_targets = [
                value
                for value in TARGET_ORDER
                if value in set(count_targets)
            ]

            return HomeIntent(
                intent_type="count_query",
                device_kind=normalized_targets[0],
                device_kinds=normalized_targets,
                confidence=0.95,
            )

    #
    # finestre
    #
    if "finestr" in lowered:
        if any(x in lowered for x in ["aperta", "aperte", "aperto", "aperti"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="window",
                desired_state="on",
                confidence=0.95,
            )

        if any(x in lowered for x in ["chiusa", "chiuse", "chiuso", "chiusi"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="window",
                desired_state="off",
                confidence=0.95,
            )

        return HomeIntent(
            intent_type="state_query",
            device_kind="window",
            confidence=0.90,
        )

    #
    # porte
    #
    if "port" in lowered:
        if any(x in lowered for x in ["aperta", "aperte", "aperto", "aperti"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="door",
                desired_state="on",
                confidence=0.95,
            )

        if any(x in lowered for x in ["chiusa", "chiuse", "chiuso", "chiusi"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="door",
                desired_state="off",
                confidence=0.95,
            )

        return HomeIntent(
            intent_type="state_query",
            device_kind="door",
            confidence=0.90,
        )

    #
    # luci
    #
    if "luce" in lowered or "luci" in lowered:
        if any(x in lowered for x in ["accesa", "accese", "accesse", "acceso", "accesi"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="light",
                desired_state="on",
                confidence=0.95,
            )

        if any(x in lowered for x in ["spenta", "spente", "spento", "spenti"]):
            return HomeIntent(
                intent_type="state_query",
                device_kind="light",
                desired_state="off",
                confidence=0.95,
            )

        if any(x in lowered for x in ["spegni", "spegni", "disattiva"]):
            return HomeIntent(
                intent_type="action",
                device_kind="light",
                action="turn_off",
                confidence=0.95,
            )

        if any(x in lowered for x in ["accendi", "attiva"]):
            return HomeIntent(
                intent_type="action",
                device_kind="light",
                action="turn_on",
                confidence=0.95,
            )

        return HomeIntent(
            intent_type="state_query",
            device_kind="light",
            confidence=0.90,
        )

    #
    # automazioni
    #
    if "automaz" in lowered:
        return HomeIntent(
            intent_type="count_query",
            device_kind="automation",
            confidence=0.95,
        )

    return HomeIntent(
        intent_type="unknown",
        confidence=0.0,
    )
