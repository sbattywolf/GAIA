from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional

EVIDENCE_CLASSES = {"OBSERVED","INFERRED","HISTORICAL","RECOMMENDED","UNRESOLVED"}
REQUIREMENT_STATES = {"AVAILABLE","UNAVAILABLE","UNKNOWN","REQUIRES_AUTHORIZATION"}
CATEGORIES = {"capability","software","runtime","model","security","validation"}

@dataclass(frozen=True)
class Observation:
    target: str
    module: str
    key: str
    value: Any
    status: str
    timestamp: str
    evidence_class: str = "OBSERVED"
    warnings: tuple[str,...] = ()
    provenance: Mapping[str,Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Evidence:
    source: str
    target: str
    module: str
    key: str
    value: Any
    status: str
    evidence_class: str
    timestamp: str
    provenance: Mapping[str,Any] = field(default_factory=dict)
    warnings: tuple[str,...] = ()

@dataclass(frozen=True)
class Requirement:
    id: str
    category: str
    name: str
    description: str = ""
    required: bool = True
    evidence_mappings: Mapping[str,str] = field(default_factory=dict)

@dataclass(frozen=True)
class RequirementResult:
    requirement_id: str
    state: str
    mapping: Optional[str] = None
    source: Optional[str] = None
    source_status: Optional[str] = None
    evidence_key: Optional[str] = None

@dataclass(frozen=True)
class Candidate:
    name: str
    source: str
    type: str
    evidence: tuple[Evidence,...] = ()
    confidence: Optional[str] = None
    rationale: str = ""
    open_questions: tuple[str,...] = ()

@dataclass(frozen=True)
class Recommendation:
    candidates: tuple[Candidate,...]
    recommendation: str
    evidence: tuple[Evidence,...]
    confidence: Optional[str] = None
    rationale: str = ""
    open_questions: tuple[str,...] = ()
    authorization_required: bool = True

def normalize_status(status: str) -> str:
    s = str(status).upper()
    if s in REQUIREMENT_STATES:
        return s
    if s == "PASS":
        return "AVAILABLE"
    if s == "FAIL":
        return "UNAVAILABLE"
    return "UNKNOWN"

def observation_to_evidence(o: Observation) -> Evidence:
    if o.evidence_class not in EVIDENCE_CLASSES:
        raise ValueError("invalid evidence class")
    return Evidence(o.source if hasattr(o,"source") else "observation",
                    o.target,o.module,o.key,o.value,normalize_status(o.status),
                    o.evidence_class,o.timestamp,o.provenance,o.warnings)

def analyze_requirement(requirement: Requirement, evidence: list[Evidence]) -> RequirementResult:
    if requirement.category not in CATEGORIES:
        raise ValueError("unsupported requirement category")
    if not requirement.required:
        return RequirementResult(requirement.id, "REQUIRES_AUTHORIZATION")
    for ev in evidence:
        if ev.key in requirement.evidence_mappings:
            return RequirementResult(requirement.id, normalize_status(ev.status),
                                     requirement.evidence_mappings[ev.key],
                                     ev.source, normalize_status(ev.status), ev.key)
    return RequirementResult(requirement.id, "UNKNOWN")

def make_recommendation(candidates, recommendation, evidence, **kwargs):
    return Recommendation(tuple(candidates), recommendation, tuple(evidence),
                          authorization_required=True, **kwargs)

def research_disabled_result():
    return ()

def sanitize_package(root: Path):
    unsafe=[]
    secret_names={".env",".env.local",".env.production",".secrets.env",".secret","secrets.env"}
    for p in root.rglob("*"):
        rel=p.relative_to(root).as_posix()
        if "__pycache__" in p.parts or (p.is_file() and (p.suffix==".pyc" or p.name in secret_names or
            p.name.endswith(".pem") or p.name.endswith(".key") or p.name.endswith(".p12"))):
            unsafe.append(rel)
    return len(unsafe)==0, unsafe
