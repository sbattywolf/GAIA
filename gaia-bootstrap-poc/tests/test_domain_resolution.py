from gaia.adapters.fake_home_assistant_adapter import FakeHomeAssistantAdapter
from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import HomeResourceReference, ObservationState, ResourceId
from gaia.home.outcomes import ClarificationRequired, ResourceAmbiguous
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


class CountingProvider(FakeHomeAssistantAdapter):
    calls = 0

    def get_opening_state(self, resource_reference):
        self.calls += 1
        return super().get_opening_state(resource_reference)


def _router_with_counting_provider():
    north = ResolvedResource(
        ResourceId("home.window.bedroom.north"),
        HomeResourceReference("window_bedroom_north"),
    )
    south = ResolvedResource(
        ResourceId("home.window.bedroom.south"),
        HomeResourceReference("window_bedroom_south"),
    )
    resolver = HomeResourceResolver({"bedroom window": (north, south)})
    provider = CountingProvider(
        {
            north.external_reference: ObservationState.CLOSED,
            south.external_reference: ObservationState.CLOSED,
        }
    )
    return RequestRouter(ReadOpeningStateCapability(resolver, provider)), provider


def test_unknown_label_requires_clarification_without_calling_provider():
    router, provider = _router_with_counting_provider()

    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "moon window")
    )

    assert outcome == ClarificationRequired(label="moon window")
    assert provider.calls == 0


def test_ambiguous_label_returns_candidates_without_calling_provider():
    router, provider = _router_with_counting_provider()

    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "bedroom window")
    )

    assert outcome == ResourceAmbiguous(
        label="bedroom window",
        candidate_ids=(
            ResourceId("home.window.bedroom.north"),
            ResourceId("home.window.bedroom.south"),
        ),
    )
    assert provider.calls == 0
