from __future__ import annotations

import os


DEFAULT_MAX_ENTITY_LIST = 10


def load_max_entity_list(
    env_value: str | None = None,
) -> int:
    value = env_value

    if value is None:
        value = os.getenv("ZEUS_MAX_ENTITY_LIST")

    if value is None:
        return DEFAULT_MAX_ENTITY_LIST

    normalized = value.strip()

    if not normalized:
        return DEFAULT_MAX_ENTITY_LIST

    try:
        parsed = int(normalized)
    except ValueError:
        return DEFAULT_MAX_ENTITY_LIST

    if parsed <= 0:
        return DEFAULT_MAX_ENTITY_LIST

    return parsed


