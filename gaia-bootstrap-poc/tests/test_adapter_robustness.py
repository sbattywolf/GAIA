from gaia.core.request_router import Request, RequestRouter
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.outcomes import Failure
from gaia.home.read_opening_state_capability import ReadOpeningStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource


class MalformedProvider:
    def get_opening_state(self, resource_reference):
        return {"state": "OPEN"}


class RaisingProvider:
    def get_opening_state(self, resource_reference):
        raise TimeoutError("simulated")


def _router(provider):
    resource = ResolvedResource(
        ResourceId("home.window.kitchen"),
        HomeResourceReference("window_kitchen"),
    )
    resolver = HomeResourceResolver({"kitchen window": (resource,)})
    return RequestRouter(ReadOpeningStateCapability(resolver, provider))


def test_malformed_provider_response_becomes_failure():
    outcome = _router(MalformedProvider()).handle(
        Request(RequestRouter.READ_OPENING_STATE, "kitchen window")
    )

    assert outcome == Failure("provider returned malformed observation")


def test_provider_exception_does_not_leak_technical_message():
    outcome = _router(RaisingProvider()).handle(
        Request(RequestRouter.READ_OPENING_STATE, "kitchen window")
    )

    assert outcome == Failure("provider failure: TimeoutError")
