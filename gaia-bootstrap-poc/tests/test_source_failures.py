from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import ObservationState, ResourceId
from gaia.home.outcomes import InformationStale, SourceUnavailable


def test_unavailable_source_remains_visible(router):
    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "garage door")
    )

    assert outcome == SourceUnavailable(ResourceId("home.door.garage"))


def test_stale_information_remains_visible(router):
    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "office window")
    )

    assert isinstance(outcome, InformationStale)
    assert outcome.resource_id == ResourceId("home.window.office")
    assert outcome.observation.state is ObservationState.STALE
