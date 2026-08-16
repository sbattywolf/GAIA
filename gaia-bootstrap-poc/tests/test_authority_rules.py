from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import ObservationState
from gaia.home.outcomes import SourceUnavailable, Success


def test_source_observation_is_the_returned_state(router):
    inferred_state = ObservationState.CLOSED

    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "kitchen window")
    )

    assert isinstance(outcome, Success)
    assert inferred_state is ObservationState.CLOSED
    assert outcome.observation.state is ObservationState.OPEN


def test_unavailable_source_is_not_replaced_by_last_known_state(router):
    last_known_state = ObservationState.OPEN

    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "garage door")
    )

    assert last_known_state is ObservationState.OPEN
    assert isinstance(outcome, SourceUnavailable)
