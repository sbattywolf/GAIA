from datetime import datetime, timezone

import pytest

from gaia.adapters.fake_home_assistant_adapter import FakeHomeAssistantAdapter
from gaia.home.models import HomeResourceReference, ObservationState


def test_fake_adapter_returns_repeatable_observation():
    reference = HomeResourceReference("window_kitchen")
    observed_at = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)
    adapter = FakeHomeAssistantAdapter(
        {reference: ObservationState.OPEN}, observed_at=observed_at
    )

    first = adapter.get_opening_state(reference)
    second = adapter.get_opening_state(reference)

    assert first == second
    assert first.observed_at == observed_at


def test_fake_adapter_has_no_fallback_for_missing_reference():
    adapter = FakeHomeAssistantAdapter({})

    with pytest.raises(LookupError):
        adapter.get_opening_state(HomeResourceReference("missing"))


def test_fake_adapter_requires_timezone_aware_observed_at():
    with pytest.raises(ValueError):
        FakeHomeAssistantAdapter({}, observed_at=datetime(2026, 8, 3, 12, 0))
