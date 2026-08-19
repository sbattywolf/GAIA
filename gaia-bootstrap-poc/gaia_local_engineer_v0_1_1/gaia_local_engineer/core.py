from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional
import hashlib
import os

DEFAULT_MAX_FILE_BYTES = 1_048_576
DEFAULT_MAX_SEARCH_RESULTS = 100
DEFAULT_MAX_LIST_RESULTS = 500
DEFAULT_MAX_READ_BYTES = 65_536
DEFAULT_MAX_DISCOVERY_ROUNDS = 3

SENSITIVE_NAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    ".secrets.env", ".secret", "secrets.env", "credentials", "credentials.json",
    "token", "tokens", "secrets", "secret",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".kdbx"}

class DiscoveryError(Exception):
    pass

class DiscoveryScopeNotAuthorized(DiscoveryError):
    pass

class PathEscapeRejected(DiscoveryError):
    pass

class SensitiveArtifactRejected(DiscoveryError):
    pass

@dataclass(frozen=True)
class DiscoveryLimits:
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_search_results: int = DEFAULT_MAX_SEARCH_RESULTS
    max_list_results: int = DEFAULT_MAX_LIST_RESULTS
    max_read_bytes: int = DEFAULT_MAX_READ_BYTES
    max_discovery_rounds: int = DEFAULT_MAX_DISCOVERY_ROUNDS

@dataclass(frozen=True)
class DiscoveryRoot:
    path: Path
    authorized: bool = True

@dataclass(frozen=True)
class Provenance:
    source_type: str
    source_path: str
    operation: str
    discovery_round: int
    discovery_root: str
    line_number: Optional[int] = None
    byte_range: Optional[tuple[int, int]] = None
    content_hash: Optional[str] = None

@dataclass(frozen=True)
class OperationResult:
    operation_status: str
    evidence_sufficiency: str
    semantic_correctness: str
    reason: Optional[str] = None
    items: tuple[Any, ...] = ()
    truncated: bool = False
    provenance: tuple[Provenance, ...] = ()

@dataclass(frozen=True)
class FileItem:
    relative_path: str
    file_type: str
    size_bytes: int

@dataclass(frozen=True)
class SearchMatch:
    relative_path: str
    line_number: int
    matched_text_or_bounded_context: str

@dataclass(frozen=True)
class ReadItem:
    relative_path: str
    content: str
    bytes_read: int
    truncated: bool

@dataclass(frozen=True)
class EvidenceRequirement:
    """Declarative, bounded evidence requirement for one unresolved question."""
    question_id: str
    required_operations: tuple[str, ...] = ()
    required_sources: int = 1


@dataclass(frozen=True)
class DiscoveryEvidence:
    observations: tuple[OperationResult, ...] = ()
    sufficient: bool = False
    semantic_correctness: str = "UNKNOWN"
    requirement: Optional[EvidenceRequirement] = None

def _canonical_root(root: DiscoveryRoot) -> Path:
    if root is None or root.path is None or not root.authorized:
        raise DiscoveryScopeNotAuthorized(
            "DISCOVERY_SCOPE_NOT_AUTHORIZED"
        )
    return root.path.expanduser().resolve(strict=True)

def _safe_relative(root: Path, candidate: Path) -> Path:
    try:
        return candidate.relative_to(root)
    except ValueError as exc:
        raise PathEscapeRejected("PATH_OUTSIDE_DISCOVERY_ROOT") from exc

def _resolve_contained(root: Path, relative_or_absolute: str | Path) -> Path:
    candidate = Path(relative_or_absolute)
    # Absolute paths are accepted only if they canonicalize inside the explicit root.
    # They are never allowed to redefine the root.
    resolved = candidate.resolve(strict=False)
    return root if resolved == root else (resolved if _safe_relative(root, resolved) is not None else resolved)

def _relative(root: Path, target: Path) -> str:
    return _safe_relative(root, target).as_posix()

def _is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    if name in SENSITIVE_NAMES:
        return True
    if any(part.lower() in SENSITIVE_NAMES for part in path.parts):
        return True
    return path.suffix.lower() in SENSITIVE_SUFFIXES

def _prov(root: Path, operation: str, target: Path, round_no: int,
          line: Optional[int] = None, byte_range: Optional[tuple[int, int]] = None,
          content_hash: Optional[str] = None) -> Provenance:
    return Provenance(
        source_type="LOCAL_FILE",
        source_path=_relative(root, target),
        operation=operation,
        discovery_round=round_no,
        discovery_root=root.as_posix(),
        line_number=line,
        byte_range=byte_range,
        content_hash=content_hash,
    )

def _escalate(reason: str) -> OperationResult:
    return OperationResult(
        operation_status="ESCALATE",
        evidence_sufficiency="INSUFFICIENT",
        semantic_correctness="UNKNOWN",
        reason=reason,
    )

def list_files(
    discovery_root: DiscoveryRoot | None,
    recursive: bool = True,
    max_results: Optional[int] = None,
    round_no: int = 1,
    limits: DiscoveryLimits = DiscoveryLimits(),
) -> OperationResult:
    try:
        root = _canonical_root(discovery_root)
    except DiscoveryScopeNotAuthorized:
        return _escalate("DISCOVERY_SCOPE_NOT_AUTHORIZED")
    limit = limits.max_list_results if max_results is None else min(max_results, limits.max_list_results)
    found: list[FileItem] = []
    provs: list[Provenance] = []
    iterator = root.rglob("*") if recursive else root.glob("*")
    for p in sorted(iterator):
        # Symlinks that resolve outside the authorized root are rejected.
        if p.is_symlink():
            target = p.resolve(strict=False)
            if target != root:
                try:
                    _safe_relative(root, target)
                except PathEscapeRejected:
                    raise
            if target.is_dir():
                continue
        if not p.is_file():
            continue
        if _is_sensitive(p):
            raise SensitiveArtifactRejected("SENSITIVE_ARTIFACT_IN_DISCOVERY_SCOPE")
        if len(found) >= limit:
            return OperationResult(
                "SUCCESS", "INSUFFICIENT", "UNKNOWN",
                items=tuple(found), truncated=True, provenance=tuple(provs)
            )
        rel = _relative(root, p.resolve(strict=False))
        found.append(FileItem(rel, "file", p.stat().st_size))
        provs.append(_prov(root, "LIST_FILES", p.resolve(strict=False), round_no))
    return OperationResult(
        "SUCCESS", "INSUFFICIENT", "UNKNOWN",
        items=tuple(found), provenance=tuple(provs)
    )

def search_text(
    discovery_root: DiscoveryRoot | None,
    query: str,
    recursive: bool = True,
    max_results: Optional[int] = None,
    round_no: int = 1,
    limits: DiscoveryLimits = DiscoveryLimits(),
) -> OperationResult:
    try:
        root = _canonical_root(discovery_root)
    except DiscoveryScopeNotAuthorized:
        return _escalate("DISCOVERY_SCOPE_NOT_AUTHORIZED")
    limit = limits.max_search_results if max_results is None else min(max_results, limits.max_search_results)
    matches: list[SearchMatch] = []
    provs: list[Provenance] = []
    iterator = root.rglob("*") if recursive else root.glob("*")
    for p in sorted(iterator):
        if p.is_symlink():
            target = p.resolve(strict=False)
            try:
                _safe_relative(root, target)
            except PathEscapeRejected:
                raise
        if not p.is_file() or _is_sensitive(p):
            continue
        if p.stat().st_size > limits.max_file_bytes:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if query in line:
                if len(matches) >= limit:
                    return OperationResult(
                        "SUCCESS", "INSUFFICIENT", "UNKNOWN",
                        items=tuple(matches), truncated=True, provenance=tuple(provs)
                    )
                resolved = p.resolve(strict=False)
                matches.append(SearchMatch(_relative(root, resolved), line_no, line[:2048]))
                digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
                provs.append(_prov(root, "SEARCH_TEXT", resolved, round_no, line_no, content_hash=digest))
    return OperationResult(
        "SUCCESS", "INSUFFICIENT", "UNKNOWN",
        items=tuple(matches), provenance=tuple(provs)
    )

def read_file(
    discovery_root: DiscoveryRoot | None,
    path: str | Path,
    max_bytes: Optional[int] = None,
    start_offset: int = 0,
    round_no: int = 1,
    limits: DiscoveryLimits = DiscoveryLimits(),
) -> OperationResult:
    try:
        root = _canonical_root(discovery_root)
    except DiscoveryScopeNotAuthorized:
        return _escalate("DISCOVERY_SCOPE_NOT_AUTHORIZED")
    candidate = Path(path)
    # Relative paths are interpreted relative to the explicit discovery root,
    # never relative to CWD. Absolute paths remain allowed only when already
    # contained by the canonical root.
    candidate_base = candidate if candidate.is_absolute() else (root / candidate)
    resolved = candidate_base.resolve(strict=False)
    _safe_relative(root, resolved)
    if _is_sensitive(resolved):
        raise SensitiveArtifactRejected("SENSITIVE_ARTIFACT_ACCESS_BLOCKED")
    if not resolved.is_file():
        return OperationResult("FAIL", "INSUFFICIENT", "UNKNOWN", reason="FILE_NOT_READABLE")
    file_size = resolved.stat().st_size
    if file_size > limits.max_file_bytes:
        return OperationResult("FAIL", "INSUFFICIENT", "UNKNOWN", reason="MAX_FILE_BYTES_EXCEEDED")
    limit = limits.max_read_bytes if max_bytes is None else min(max_bytes, limits.max_read_bytes)
    with resolved.open("rb") as fh:
        fh.seek(max(0, start_offset))
        data = fh.read(limit)
        extra = fh.read(1)
    truncated = bool(extra)
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        return OperationResult("FAIL", "INSUFFICIENT", "UNKNOWN", reason="NON_TEXT_FILE")
    digest = hashlib.sha256(data).hexdigest()
    item = ReadItem(_relative(root, resolved), content, len(data), truncated)
    return OperationResult(
        "SUCCESS", "INSUFFICIENT", "UNKNOWN", items=(item,), truncated=truncated,
        provenance=(_prov(root, "READ_FILE", resolved, round_no,
                          byte_range=(start_offset, start_offset + len(data)),
                          content_hash=digest),)
    )

def assess_evidence_sufficiency(
    results: Iterable[OperationResult],
    required_sources: int = 1,
    semantic_correctness: str = "UNKNOWN",
    requirement: Optional[EvidenceRequirement] = None,
) -> DiscoveryEvidence:
    """Assess primitive availability, optionally against a declarative question requirement.

    This does not determine semantic correctness. A successful operation is not, by itself,
    sufficient evidence for a question unless the supplied bounded requirement is satisfied.
    """
    material = tuple(results)
    usable = [
        r for r in material
        if r.operation_status == "SUCCESS" and bool(r.items) and not r.truncated
    ]
    if requirement is None:
        sufficient = len(usable) >= required_sources
    else:
        required_ops = set(requirement.required_operations)
        # Operation provenance is the authoritative bounded indicator of what evidence was produced.
        pertinent = [
            r for r in usable
            if not required_ops or any(p.operation in required_ops for p in r.provenance)
        ]
        sufficient = len(pertinent) >= requirement.required_sources
    return DiscoveryEvidence(
        material, sufficient, semantic_correctness if sufficient else "UNKNOWN", requirement
    )


def _round_has_pertinent_evidence(
    results: Iterable[OperationResult],
    requirement: EvidenceRequirement | None,
) -> bool:
    if requirement is None:
        return False
    return assess_evidence_sufficiency(
        results, requirement=requirement
    ).sufficient

def discovery_loop(
    discovery_root: DiscoveryRoot | None,
    rounds: Iterable[tuple[str, Any]],
    limits: DiscoveryLimits = DiscoveryLimits(),
    requirement: EvidenceRequirement | None = None,
) -> tuple[OperationResult, ...]:
    """Run predeclared bounded discovery operations with explicit round admission.

    A subsequent round is admitted only when the preceding round produced pertinent
    evidence for the supplied unresolved question. No new operations are invented.
    """
    if discovery_root is None or not discovery_root.authorized:
        return (_escalate("DISCOVERY_SCOPE_NOT_AUTHORIZED"),)
    if requirement is None:
        return ()
    planned_rounds = tuple(rounds)
    outputs: list[OperationResult] = []
    current_round: list[OperationResult] = []
    current_round_no = 0
    for operation, args in planned_rounds:
        requested_round = current_round_no + 1
        if requested_round > limits.max_discovery_rounds:
            outputs.append(_escalate("DISCOVERY_BUDGET_EXHAUSTED"))
            break
        if current_round_no > 0 and not _round_has_pertinent_evidence(current_round, requirement):
            break
        if requested_round > 1:
            current_round = []
        if operation == "LIST_FILES":
            result = list_files(discovery_root, round_no=requested_round, limits=limits, **args)
        elif operation == "SEARCH_TEXT":
            result = search_text(discovery_root, round_no=requested_round, limits=limits, **args)
        elif operation == "READ_FILE":
            result = read_file(discovery_root, round_no=requested_round, limits=limits, **args)
        else:
            result = _escalate("UNSUPPORTED_DISCOVERY_OPERATION")
        outputs.append(result)
        current_round.append(result)
        current_round_no = requested_round
    if current_round_no >= limits.max_discovery_rounds and len(outputs) < len(planned_rounds):
        outputs.append(_escalate("DISCOVERY_BUDGET_EXHAUSTED"))
    return tuple(outputs)

def sanitize_delivery(root: Path) -> tuple[bool, tuple[str, ...]]:
    unsafe: list[str] = []
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        if "__pycache__" in p.parts or (p.is_file() and (p.suffix.lower() == ".pyc" or _is_sensitive(p))):
            unsafe.append(rel)
    return not unsafe, tuple(sorted(unsafe))
