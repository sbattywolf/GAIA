from gaia.core.request_router import Request
from gaia.home.outcomes import Unsupported


def test_unsupported_operation_is_rejected_without_execution(router):
    outcome = router.handle(Request("open_door", "garage door"))

    assert outcome == Unsupported(operation="open_door")
