from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

from datetime import datetime, timedelta, timezone

from gaia.adapters.light_contracts import MalformedLightProviderResponse
from gaia.core.request_router import Request, RequestRouter
from gaia.home.collaborator import HomeCollaborator
from gaia.home.light_models import LightObservation, LightObservationState
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.read_current_resource_state import ReadCurrentResourceStateCapability
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource
from gaia.home.w3_outcomes import (
    ApprovalRequired, CurrentStateSuccess, Denied, ExecutionFailure,
    Indeterminate, InformationStale, SourceUnavailable,
)

RESOURCE = ResolvedResource(ResourceId("home.light.living_room"), HomeResourceReference("light.living_room"))

class FakeProvider:
    def __init__(self, observation=None, error=None):
        self.observation = observation
        self.error = error
        self.calls = 0
    def get_light_state(self, reference):
        self.calls += 1
        if self.error:
            raise self.error
        return self.observation

def router(provider):
    resolver = HomeResourceResolver({"living-room light": (RESOURCE,)})
    cap = ReadCurrentResourceStateCapability(resolver, provider)
    return RequestRouter(home_collaborator=HomeCollaborator(cap))

def observation(state, when=None):
    return LightObservation(RESOURCE.resource_id, RESOURCE.external_reference, state, when or datetime.now(timezone.utc))

def test_pm2_t04_normal_light_read_is_source_grounded():
    p = FakeProvider(observation(LightObservationState.ON))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light"))
    assert isinstance(out, CurrentStateSuccess)
    assert out.observation.state is LightObservationState.ON
    assert out.observation.resource_id == RESOURCE.resource_id
    assert p.calls == 1

def test_pm2_t06_unavailable_is_explicit():
    p = FakeProvider(observation(LightObservationState.UNAVAILABLE))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light"))
    assert isinstance(out, SourceUnavailable)
    assert p.calls == 1

def test_pm2_t07_stale_is_explicit():
    p = FakeProvider(observation(LightObservationState.STALE))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light"))
    assert isinstance(out, InformationStale)
    assert p.calls == 1

def test_pm2_t07_malformed_provider_error_is_explicit():
    p = FakeProvider(error=MalformedLightProviderResponse("bad response"))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light"))
    assert isinstance(out, ExecutionFailure)
    assert "bad response" in out.reason
    assert p.calls == 1

def test_pm2_t08_denied_blocks_capability_and_provider():
    p = FakeProvider(observation(LightObservationState.ON))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light", policy_result="Denied"))
    assert isinstance(out, Denied)
    assert p.calls == 0

def test_pm2_t08_indeterminate_blocks_capability_and_provider():
    p = FakeProvider(observation(LightObservationState.ON))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light", policy_result="Indeterminate"))
    assert isinstance(out, Indeterminate)
    assert p.calls == 0

def test_pm2_t08_required_not_granted_blocks_capability_and_provider():
    p = FakeProvider(observation(LightObservationState.ON))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light", approval="Required"))
    assert isinstance(out, ApprovalRequired)
    assert p.calls == 0

def test_pm2_t08_required_granted_executes_once():
    p = FakeProvider(observation(LightObservationState.OFF))
    out = router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE, "living-room light", approval="Required", approval_granted=True))
    assert isinstance(out, CurrentStateSuccess)
    assert p.calls == 1

def test_pm2_t09_disabled_control_has_no_external_read(tmp_path, monkeypatch):
    import subprocess
    state = tmp_path / "state"
    monkeypatch.setenv("GAIA_PM002_STATE_DIR", str(state))
    script = "scripts/pm002_stop.sh"
    result = subprocess.run([script], cwd=str(PROJECT_ROOT), text=True, capture_output=True)
    assert result.returncode == 0
    assert (state / "disabled").exists()
    assert "external read" in result.stdout.lower() or "read" in result.stdout.lower()

def test_pm2_t12_scripts_do_not_contain_literal_credentials():
    from pathlib import Path
    root = Path("gaia-bootstrap-poc/scripts")
    for path in root.glob("pm002_*.sh"):
        text = path.read_text()
        assert "Bearer ey" not in text
        assert "ghp_" not in text
        assert "sk-" not in text

def test_pm2_t14_evidence_manifest_is_sanitized_and_reconstructable():
    from pathlib import Path
    evidence = Path("PM002_EVIDENCE.md").read_text()
    manifest = Path("PM002_IMPLEMENTATION_MANIFEST.md").read_text()
    for forbidden in ("Bearer ey", "ghp_", "sk-"):
        assert forbidden not in evidence
        assert forbidden not in manifest
    assert "f01a13a8fd6258f0f568b1ceecea82c9b8a62aa8" in manifest
    assert "PM2-T01" in evidence and "PM2-T14" in evidence
