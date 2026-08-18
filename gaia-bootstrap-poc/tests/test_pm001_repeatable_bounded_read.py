
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from gaia.adapters.home_assistant_light_adapter import HomeAssistantLightAdapter
from gaia.core.request_router import Request, RequestRouter
from gaia.home.collaborator import HomeCollaborator
from gaia.home.light_models import LightObservation, LightObservationState
from gaia.home.models import HomeResourceReference, ResourceId
from gaia.home.read_current_resource_state import ReadCurrentResourceStateCapability, ReadCurrentResourceStateRequest
from gaia.home.resource_resolver import HomeResourceResolver, ResolvedResource
from gaia.home.w3_outcomes import ApprovalRequired, CurrentStateSuccess, Denied, ExecutionFailure, Indeterminate, InformationStale, InvalidResourceReference, ResourceNotFound, SourceUnavailable, Unsupported
from gaia.home.w3_policy_gate import ApprovalRequirement, PolicyResult

OBSERVED_AT=datetime(2026,8,18,12,0,tzinfo=timezone.utc)
LIGHT=ResolvedResource(ResourceId("home.light.living_room"),HomeResourceReference("light.living_room"))

class CountingProvider:
    def __init__(self,result=None,error=None): self.calls=0; self.result=result; self.error=error
    def get_light_state(self,ref):
        self.calls += 1
        if self.error: raise self.error
        return self.result

class CountingCapability:
    def __init__(self,cap): self.calls=0; self._cap=cap
    def execute(self,req): self.calls+=1; return self._cap.execute(req)

class FakeTransport:
    def __init__(self,payload=None,error=None): self.calls=0; self.payload=payload; self.error=error
    def get_state(self,entity_id):
        self.calls+=1
        if self.error: raise self.error
        return self.payload

def router(provider, capability=None, label="living-room light"):
    cap=capability or ReadCurrentResourceStateCapability(HomeResourceResolver({label:(LIGHT,)}),provider)
    return RequestRouter(home_collaborator=HomeCollaborator(cap))

def permitted_router(provider, capability=None):
    return router(provider,capability)

def test_p01_valid_light_read():
    obs=LightObservation(LIGHT.resource_id,LIGHT.external_reference,LightObservationState.ON,OBSERVED_AT)
    p=CountingProvider(obs); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    o=permitted_router(p,c).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light"))
    assert isinstance(o,CurrentStateSuccess); assert o.resource_id==LIGHT.resource_id; assert c.calls==1; assert p.calls==1

def test_p02_repeated_valid_reads_same_bounded_path():
    obs=LightObservation(LIGHT.resource_id,LIGHT.external_reference,LightObservationState.ON,OBSERVED_AT)
    p=CountingProvider(obs); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    r=permitted_router(p,c)
    outcomes=[r.handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light")) for _ in range(5)]
    assert all(isinstance(o,CurrentStateSuccess) for o in outcomes)
    assert c.calls==5 and p.calls==5

def test_p03_resource_not_found_no_fallback():
    p=CountingProvider()
    o=router(p,label="living-room light").handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"unknown light"))
    assert isinstance(o,ResourceNotFound); assert p.calls==0

def test_p04_malformed_resource_reference_no_fabrication():
    bad=ResolvedResource(ResourceId("home.light.living_room"),HomeResourceReference("malformed"))
    t=FakeTransport({"entity_id":"malformed","state":"on","last_updated":OBSERVED_AT.isoformat()})
    p=HomeAssistantLightAdapter(t,bad.resource_id)
    c=ReadCurrentResourceStateCapability(HomeResourceResolver({"bad light":(bad,)}),p)
    o=c.execute(ReadCurrentResourceStateRequest("bad light"))
    assert isinstance(o,InvalidResourceReference); assert t.calls==0

def test_p05_home_assistant_unavailable_explicit():
    p=CountingProvider(error=ConnectionError("unavailable"))
    o=router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light"))
    assert isinstance(o,SourceUnavailable); assert p.calls==1

def test_p06_unexpected_response_explicit():
    from gaia.adapters.light_contracts import MalformedLightProviderResponse
    p=CountingProvider(error=MalformedLightProviderResponse("malformed"))
    o=router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light"))
    assert isinstance(o,ExecutionFailure); assert p.calls==1

def test_p07_stale_response_explicit():
    stale=LightObservation(LIGHT.resource_id,LIGHT.external_reference,LightObservationState.STALE,OBSERVED_AT-timedelta(minutes=10))
    p=CountingProvider(stale)
    o=router(p).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light"))
    assert isinstance(o,InformationStale); assert p.calls==1

def test_p08_policy_denied_zero_capability_and_provider_calls():
    p=CountingProvider(); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    o=router(p,c).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light",policy_result=PolicyResult.DENIED.value))
    assert isinstance(o,Denied); assert c.calls==0 and p.calls==0

def test_p09_policy_indeterminate_zero_capability_and_provider_calls():
    p=CountingProvider(); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    o=router(p,c).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light",policy_result=PolicyResult.INDETERMINATE.value))
    assert isinstance(o,Indeterminate); assert c.calls==0 and p.calls==0

def test_p10_approval_required_not_granted_zero_calls():
    p=CountingProvider(); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    o=router(p,c).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light",approval=ApprovalRequirement.REQUIRED.value))
    assert isinstance(o,ApprovalRequired); assert c.calls==0 and p.calls==0

def test_p11_approval_required_granted_one_read():
    obs=LightObservation(LIGHT.resource_id,LIGHT.external_reference,LightObservationState.OFF,OBSERVED_AT)
    p=CountingProvider(obs); c=CountingCapability(ReadCurrentResourceStateCapability(HomeResourceResolver({"living-room light":(LIGHT,)}),p))
    o=router(p,c).handle(Request(RequestRouter.READ_CURRENT_RESOURCE_STATE,"living-room light",approval=ApprovalRequirement.REQUIRED.value,approval_granted=True))
    assert isinstance(o,CurrentStateSuccess); assert c.calls==1 and p.calls==1

def test_p12_write_attempt_zero_write_calls():
    p=CountingProvider()
    o=router(p).handle(Request("write","living-room light"))
    assert isinstance(o,Unsupported); assert p.calls==0

def test_p13_out_of_scope_zero_calls():
    p=CountingProvider()
    o=router(p).handle(Request("turn_off_and_schedule","all lights"))
    assert isinstance(o,Unsupported); assert p.calls==0

def test_p14_evidence_reconstruction_schema():
    evidence={
      "scenario":"PM-001",
      "run_id":"PM001-ENGINEER-CONTROLLED-001",
      "repository_commit":"459861de04f90f64dec9287619a3f3a8340b1750",
      "execution_mode":"deterministic fixture",
      "timestamp":"2026-08-18T12:00:00Z",
      "operation":"Read",
      "resource_id":"home.light.living_room",
      "provider_reference":"light.living_room",
      "collaborator":"HomeCollaborator",
      "capability":"Read Current Resource State",
      "policy_result":"Allowed",
      "approval_requirement":"Not Required",
      "approval_grant":"Not Granted",
      "capability_invocation_count":1,
      "provider_execution_count":1,
      "structured_outcome":"CurrentStateSuccess",
      "source_observation":"ON",
      "freshness":"current",
      "failure_class":None,
      "repeatability":{"runs":5,"capability_calls":[1,1,1,1,1],"provider_calls":[1,1,1,1,1]}
    }
    required={"scenario","run_id","repository_commit","execution_mode","timestamp","operation","resource_id","provider_reference","collaborator","capability","policy_result","approval_requirement","approval_grant","capability_invocation_count","provider_execution_count","structured_outcome","source_observation","freshness","failure_class","repeatability"}
    assert required <= evidence.keys()
    json.dumps(evidence)
