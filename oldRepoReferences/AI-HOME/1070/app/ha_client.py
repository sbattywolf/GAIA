from dataclasses import dataclass, field

import httpx


@dataclass
class EntityQuery:
    domain: str = None
    device_classes: list = field(default_factory=list)
    states: list = field(default_factory=list)
    name_terms: list = field(default_factory=list)


class HAClient:
    def __init__(
        self,
        base_url,
        token,
        agent_id=None,
        timeout=120,
    ):
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id.strip() if agent_id else None
        self.timeout = timeout
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        }

    async def get_states(self):
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                self.base_url + "/api/states",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def query_entities(self, query):
        states = await self.get_states()
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

        for item in states:
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

    async def process_conversation(
        self,
        text,
        conversation_id=None,
        language="it",
    ):
        payload = {
            "text": text,
            "language": language,
        }

        if self.agent_id:
            payload["agent_id"] = self.agent_id

        if conversation_id:
            payload["conversation_id"] = conversation_id

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:
            response = await client.post(
                self.base_url + "/api/conversation/process",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        response_data = data.get("response", {})

        speech = (
            response_data
            .get("speech", {})
            .get("plain", {})
            .get("speech")
        )

        if not speech:
            speech = (
                response_data
                .get("data", {})
                .get("message")
                or "Home Assistant non ha restituito una risposta."
            )

        return (
            speech,
            data.get("conversation_id"),
            response_data.get("response_type", "unknown"),
        )


def format_entity_results(results, state_label=None):
    if not results:
        return "Non risultano entità corrispondenti alla richiesta."

    names = [item["name"] for item in results]

    if len(names) == 1:
        formatted_names = names[0]
    else:
        formatted_names = ", ".join(names[:-1]) + " e " + names[-1]

    if state_label:
        return f"Risultano {state_label}: {formatted_names}."

    return formatted_names + "."
