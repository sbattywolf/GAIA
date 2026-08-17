from __future__ import annotations

import json
from collections.abc import Mapping
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


class HomeAssistantHTTPTransport:
    """Minimal synchronous transport for one Home Assistant state read.

    Runtime configuration is supplied by the caller. No credentials are
    persisted, logged, or embedded in GAIA contracts.
    """

    def __init__(self, base_url: str, bearer_token: str, timeout: float = 5.0):
        self._base_url = base_url.rstrip("/")
        self._bearer_token = bearer_token
        self._timeout = timeout

    def get_state(self, entity_id: str) -> Mapping[str, object]:
        encoded_entity_id = quote(entity_id, safe="")
        request = Request(
            f"{self._base_url}/api/states/{encoded_entity_id}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._bearer_token}",
            },
            method="GET",
        )

        with urlopen(request, timeout=self._timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if not isinstance(payload, Mapping):
            raise ValueError("Home Assistant response is not an object")

        return payload
