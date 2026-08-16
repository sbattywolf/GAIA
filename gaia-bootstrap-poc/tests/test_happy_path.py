from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import ObservationState, ResourceId
from gaia.home.outcomes import Success


def test_kitchen_window_is_open(router):
    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "kitchen window")
    )

    assert isinstance(outcome, Success)
    assert outcome.resource_id == ResourceId("home.window.kitchen")
    assert outcome.observation.state is ObservationState.OPEN


def test_front_door_is_closed(router):
    outcome = router.handle(
        Request(RequestRouter.READ_OPENING_STATE, "front door")
    )

    assert isinstance(outcome, Success)
    assert outcome.resource_id == ResourceId("home.door.front")
    assert outcome.observation.state is ObservationState.CLOSED
