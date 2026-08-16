from datetime import datetime, timezone

from gaia.adapters.contracts import OpeningStateProvider
from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import HomeResourceReference, Observation, ObservationState, ResourceId
from gaia.home.outcomes import Success
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


class AlternativeProvider:
    def get_opening_state(self, resource_reference):
        return Observation(
            resource_reference=resource_reference,
            state=ObservationState.CLOSED,
            observed_at=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc),
        )


def test_provider_can_be_replaced_without_changing_core_or_domain_flow():
    resource = ResolvedResource(
        ResourceId("home.window.kitchen"),
        HomeResourceReference("alternative_window_reference"),
    )
    resolver = HomeResourceResolver({"kitchen window": (resource,)})
    provider: OpeningStateProvider = AlternativeProvider()
    router = RequestRouter(ReadOpeningStateCapability(resolver, provider))

    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "kitchen window")
    )

    assert isinstance(outcome, Success)
    assert outcome.observation.state is ObservationState.CLOSED
