from __future__ import annotations

from datetime import datetime, timedelta, timezone

from gaia.adapters.home_assistant_light_adapter import HomeAssistantLightAdapter
from gaia.core.request_router import Request, RequestRouter
from gaia.home.collaborator import HomeCollaborator
from gaia.home.light_models import LightObservation, LightObservationState
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.read_current_resource_state import (
    ReadCurrentResourceStateCapability,
    ReadCurrentResourceStateRequest,
)
from gaia.home.w3_policy_gate import ApprovalRequirement, PolicyResult
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource
from gaia.home.w3_outcomes import (
    ApprovalRequired,
    CurrentStateSuccess,
    Denied,
    ExecutionFailure,
    Indeterminate,
    InformationStale,
    InvalidResourceReference,
    ResourceNotFound,
    SourceUnavailable,
    Unsupported,
)


OBSERVED_AT = datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc)
LIGHT = ResolvedResource(
    resource_id=ResourceId("home.light.living_room"),
    external_reference=HomeResourceReference("light.living_room"),
)


class CountingLightProvider:
    def __init__(self, result=None, error=None):
        self.calls = 0
        self.result = result
        self.error = error

    def get_light_state(self, resource_reference):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.result


class CountingCapability:
    def __init__(self, capability):
        self.calls = 0
        self._capability = capability

    def execute(self, request):
        self.calls += 1
        return self._capability.execute(request)


class FakeTransport:
    def __init__(self, payload=None, error=None):
        self.calls = 0
        self.payload = payload
        self.error = error

    def get_state(self, entity_id):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.payload


def build_router(provider, capability=None):
    resolver = HomeResourceResolver({"living-room light": (LIGHT,)})
    capability = capability or ReadCurrentResourceStateCapability(resolver, provider)
    collaborator = HomeCollaborator(capability)
    return RequestRouter(home_collaborator=collaborator)


def test_t01_valid_light_read():
    transport = FakeTransport(
        {
            "entity_id": "light.living_room",
            "state": "on",
            "last_updated": OBSERVED_AT.isoformat(),
        }
    )
    provider = HomeAssistantLightAdapter(
        transport,
        LIGHT.resource_id,
    )
    capability = CountingCapability(
        ReadCurrentResourceStateCapability(
            HomeResourceResolver({"living-room light": (LIGHT,)}), provider
        )
    )
    router = build_router(provider, capability)

    outcome = router.handle(
        Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light")
    )

    assert isinstance(outcome, CurrentStateSuccess)
    assert outcome.observation.state is LightObservationState.ON
    assert capability.calls == 1
    assert transport.calls == 1


def test_t02_light_entity_not_found():
    provider = CountingLightProvider()
    router = build_router(provider)

    outcome = router.handle(
        Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "unknown light")
    )

    assert isinstance(outcome, ResourceNotFound)
    assert provider.calls == 0


def test_t03_malformed_identifier():
    malformed = ResolvedResource(
        resource_id=ResourceId("home.light.malformed"),
        external_reference=HomeResourceReference("not-an-entity-id"),
    )
    transport = FakeTransport(
        {
            "entity_id": "not-an-entity-id",
            "state": "on",
            "last_updated": OBSERVED_AT.isoformat(),
        }
    )
    provider = HomeAssistantLightAdapter(
        transport,
        malformed.resource_id,
    )
    resolver = HomeResourceResolver({"malformed light": (malformed,)})
    capability = ReadCurrentResourceStateCapability(resolver, provider)

    outcome = capability.execute(
        ReadCurrentResourceStateRequest(label="malformed light")
    )

    assert isinstance(outcome, InvalidResourceReference)
    assert transport.calls == 0


def test_t04_home_assistant_unavailable():
    transport = FakeTransport(error=ConnectionError("unavailable"))
    provider = HomeAssistantLightAdapter(
        transport,
        LIGHT.resource_id,
    )
    router = build_router(provider)

    outcome = router.handle(
        Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light")
    )

    assert isinstance(outcome, SourceUnavailable)
    assert transport.calls == 1


def test_t05_unexpected_external_response():
    transport = FakeTransport({"entity_id": "light.living_room"})
    provider = HomeAssistantLightAdapter(
        transport,
        LIGHT.resource_id,
    )
    router = build_router(provider)

    outcome = router.handle(
        Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light")
    )

    assert isinstance(outcome, ExecutionFailure)
    assert transport.calls == 1


def test_t06_stale_response_is_not_current():
    stale_at = OBSERVED_AT - timedelta(minutes=10)
    transport = FakeTransport(
        {
            "entity_id": "light.living_room",
            "state": "on",
            "last_updated": stale_at.isoformat(),
        }
    )
    provider = HomeAssistantLightAdapter(
        transport,
        LIGHT.resource_id,
        max_age=timedelta(minutes=5),
        now=lambda: OBSERVED_AT,
    )
    router = build_router(provider)

    outcome = router.handle(
        Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light")
    )

    assert isinstance(outcome, InformationStale)
    assert transport.calls == 1


def test_t07_write_attempt_never_executes():
    provider = CountingLightProvider()
    router = build_router(provider)

    outcome = router.handle(Request("write", "living-room light"))

    assert isinstance(outcome, Unsupported)
    assert provider.calls == 0


def test_t08_out_of_scope_request_never_expands():
    provider = CountingLightProvider()
    router = build_router(provider)

    outcome = router.handle(
        Request("turn_off_and_schedule", "all lights")
    )

    assert isinstance(outcome, Unsupported)
    assert provider.calls == 0


def test_t09_policy_denied_and_indeterminate_never_execute():
    for policy_result, expected_type in (
        (PolicyResult.DENIED, Denied),
        (PolicyResult.INDETERMINATE, Indeterminate),
    ):
        provider = CountingLightProvider()
        capability = CountingCapability(
            ReadCurrentResourceStateCapability(
                HomeResourceResolver({"living-room light": (LIGHT,)}), provider
            )
        )
        router = build_router(provider, capability)

        outcome = router.handle(
            Request(
                RequestRouter.READ_CURRENT_RESOURCE_STATE,
                "living-room light",
                policy_result=policy_result.value,
            )
        )

        assert isinstance(outcome, expected_type)
        assert capability.calls == 0
        assert provider.calls == 0


def test_t10_approval_required_blocks_without_grant_but_grant_executes():
    blocked_provider = CountingLightProvider()
    blocked_capability = CountingCapability(
        ReadCurrentResourceStateCapability(
            HomeResourceResolver({"living-room light": (LIGHT,)}), blocked_provider
        )
    )
    blocked_router = build_router(blocked_provider, blocked_capability)

    blocked = blocked_router.handle(
        Request(
            RequestRouter.READ_CURRENT_RESOURCE_STATE,
            "living-room light",
            approval=ApprovalRequirement.REQUIRED.value,
            approval_granted=False,
        )
    )

    assert isinstance(blocked, ApprovalRequired)
    assert blocked_capability.calls == 0
    assert blocked_provider.calls == 0

    granted_observation = LightObservation(
        resource_id=LIGHT.resource_id,
        resource_reference=LIGHT.external_reference,
        state=LightObservationState.OFF,
        observed_at=OBSERVED_AT,
    )
    granted_provider = CountingLightProvider(result=granted_observation)
    granted_capability = CountingCapability(
        ReadCurrentResourceStateCapability(
            HomeResourceResolver({"living-room light": (LIGHT,)}), granted_provider
        )
    )
    granted_router = build_router(granted_provider, granted_capability)

    granted = granted_router.handle(
        Request(
            RequestRouter.READ_CURRENT_RESOURCE_STATE,
            "living-room light",
            approval=ApprovalRequirement.REQUIRED.value,
            approval_granted=True,
        )
    )

    assert isinstance(granted, CurrentStateSuccess)
    assert granted_capability.calls == 1
    assert granted_provider.calls == 1
