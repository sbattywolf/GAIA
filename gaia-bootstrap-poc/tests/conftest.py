from __future__ import annotations

import pytest

from gaia.bootstrap import build_bootstrap_router


@pytest.fixture
def router():
    return build_bootstrap_router()
