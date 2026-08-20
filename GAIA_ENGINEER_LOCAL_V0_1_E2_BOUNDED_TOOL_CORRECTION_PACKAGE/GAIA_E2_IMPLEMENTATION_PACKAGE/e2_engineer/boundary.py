"""Bounded filesystem, validation, and Git-inspection contracts for E2.

This module intentionally contains no shell gateway and no Git mutation API.
It is a small local continuity/tool boundary, not a GAIA production layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Iterable, Sequence


class BoundaryViolation(RuntimeError):
    """Base class for an E2 boundary rejection."""


class WorkspaceEscapeBlocked(BoundaryViolation):
    """The requested path resolves outside the authorized workspace."""


class SecretPathBlocked(BoundaryViolation):
    """The requested path is configured as sensitive/secret."""


class ProtectedPathBlocked(BoundaryViolation):
    """The requested write targets a protected repository path."""


class GitMutationBlocked(BoundaryViolation):
    """Git mutation is intentionally unavailable in E2."""


@dataclass(frozen=True)
class RunTestsPolicy:
    """Allowlist for the dedicated validation operation.

    Commands are tokenized and matched as complete command forms. No shell
    parsing or shell execution is used, so pipes/redirection/substitution are
    not available through this API.
    """

    allowed_commands: tuple[tuple[str, ...], ...] = (
        ("python", "-m", "pytest"),
        ("pytest",),
    )
    allowed_pytest_args: tuple[str, ...] = (
        "-q", "-v", "--quiet", "--verbose",
        "-x", "--maxfail", "--tb=short", "--tb=long",
        "--disable-warnings", "--no-header", "--no-summary",
    )

    def validate(self, command: Sequence[str]) -> tuple[str, ...]:
        tokens = tuple(command)
        if not tokens:
            raise BoundaryViolation("run_tests requires a non-empty command")
        if any(not isinstance(t, str) or not t for t in tokens):
            raise BoundaryViolation("run_tests command tokens must be non-empty strings")
        if any(t in {";", "&&", "||", "|", ">", ">>", "<"} for t in tokens):
            raise BoundaryViolation("shell operators are not permitted by run_tests")
        if any("$" in t or "`" in t for t in tokens):
            raise BoundaryViolation("shell expansion is not permitted by run_tests")
        prefix = next((p for p in self.allowed_commands if tokens[:len(p)] == p), None)
        if prefix is None:
            raise BoundaryViolation(f"command form is not authorized: {tokens!r}")

        # E2 permits only bounded test selection and output-control arguments.
        # Pytest configuration, plugin, import-path, environment, and generic
        # execution options are intentionally outside this contract.
        for token in tokens[len(prefix):]:
            if token.startswith("-"):
                if token.startswith("--maxfail="):
                    value = token.split("=", 1)[1]
                    if not value.isdigit() or value == "0":
                        raise BoundaryViolation("--maxfail requires a positive integer")
                    continue
                if token not in self.allowed_pytest_args:
                    raise BoundaryViolation(f"pytest argument is not authorized: {token!r}")
            elif not token:
                raise BoundaryViolation("empty pytest path is not permitted")
        return tokens


_DEFAULT_SENSITIVE = (
    ".secrets.env",
    "secrets.env",
    ".ssh",
    ".aws",
    ".gnupg",
    ".config/gaia/.secrets.env",
)


@dataclass
class EngineerWorkspace:
    """Technically enforced E2 workspace boundary."""

    root: Path
    protected_paths: Iterable[str] = ()
    sensitive_paths: Iterable[str] = _DEFAULT_SENSITIVE
    test_policy: RunTestsPolicy = RunTestsPolicy()

    def __post_init__(self) -> None:
        self.root = self.root.expanduser().resolve(strict=True)
        self._protected = tuple(self._normalize_pattern(p) for p in self.protected_paths)
        self._sensitive = tuple(self._normalize_pattern(p) for p in self.sensitive_paths)

    @staticmethod
    def _normalize_pattern(value: str) -> str:
        value = value.replace("\\", "/").strip("/")
        return value

    def _resolved(self, relative_path: str | Path) -> Path:
        candidate = Path(relative_path)
        if candidate.is_absolute():
            resolved = candidate.resolve(strict=False)
        else:
            resolved = (self.root / candidate).resolve(strict=False)
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise WorkspaceEscapeBlocked(
                f"path resolves outside authorized workspace: {relative_path!s}"
            ) from exc
        return resolved

    def _matches(self, resolved: Path, patterns: tuple[str, ...]) -> bool:
        rel = resolved.relative_to(self.root).as_posix()
        for pattern in patterns:
            if not pattern:
                continue
            if rel == pattern or rel.startswith(pattern + "/"):
                return True
            if Path(rel).name == pattern:
                return True
        return False

    def authorize_read(self, relative_path: str | Path) -> Path:
        resolved = self._resolved(relative_path)
        if self._matches(resolved, self._sensitive):
            raise SecretPathBlocked(f"sensitive path is not readable: {relative_path!s}")
        return resolved

    def authorize_write(self, relative_path: str | Path) -> Path:
        resolved = self._resolved(relative_path)
        if self._matches(resolved, self._sensitive):
            raise SecretPathBlocked(f"sensitive path is not writable: {relative_path!s}")
        if self._matches(resolved, self._protected):
            raise ProtectedPathBlocked(f"protected path is not writable: {relative_path!s}")
        return resolved

    def read_file(self, relative_path: str | Path, encoding: str = "utf-8") -> str:
        return self.authorize_read(relative_path).read_text(encoding=encoding)

    def write_file(self, relative_path: str | Path, content: str, encoding: str = "utf-8") -> Path:
        target = self.authorize_write(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding=encoding)
        return target

    def search(self, pattern: str, *, glob: str = "**/*") -> list[tuple[str, int, str]]:
        if not pattern:
            raise BoundaryViolation("search pattern must be non-empty")
        rx = re.compile(pattern)
        results: list[tuple[str, int, str]] = []
        for path in self.root.glob(glob):
            if not path.is_file():
                continue
            try:
                authorized = self.authorize_read(path)
            except BoundaryViolation:
                continue
            try:
                text = authorized.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for line_no, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    results.append((authorized.relative_to(self.root).as_posix(), line_no, line))
        return results

    def run_tests(self, command: Sequence[str], *, timeout: int = 300) -> subprocess.CompletedProcess[str]:
        tokens = self.test_policy.validate(command)
        for token in tokens[len(next(prefix for prefix in self.test_policy.allowed_commands if tokens[:len(prefix)] == prefix)) :]:
            if token.startswith("-"):
                if "=" in token and token.split("=", 1)[1].startswith("/"):
                    raise WorkspaceEscapeBlocked("absolute validation path is not permitted")
                continue
            if Path(token).is_absolute() or token == ".." or token.startswith("../") or "/" in token:
                self._resolved(token)
        return subprocess.run(
            list(tokens),
            cwd=self.root,
            text=True,
            capture_output=True,
            shell=False,
            timeout=timeout,
            check=False,
        )

    def _authorize_git_path_argument(self, token: str) -> None:
        # Git pathspecs may be absolute, relative, or use parent traversal.
        # Validate only arguments in the path-bearing portions of the
        # read-only inspection commands; option values remain options.
        if not token or token.startswith("-"):
            return
        if token == "--":
            return
        if token.startswith(":"):
            return
        if token.endswith(":") and token.count(":") == 1:
            return
        self.authorize_read(token)

    def git_inspect(self, args: Sequence[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
        tokens = tuple(args)
        if not tokens:
            raise BoundaryViolation("git inspection requires an operation")
        allowed = {"status", "diff", "log"}
        if tokens[0] not in allowed:
            raise GitMutationBlocked(f"git operation is not available in E2: {tokens[0]}")

        # Only the explicitly read-only Git operations are exposed. Any
        # filesystem path represented by their arguments is resolved through
        # the same workspace boundary used by the filesystem tools.
        for token in tokens[1:]:
            self._authorize_git_path_argument(token)

        return subprocess.run(
            ["git", *tokens],
            cwd=self.root,
            text=True,
            capture_output=True,
            shell=False,
            timeout=timeout,
            check=False,
        )

    def git_mutate(self, *_args: str, **_kwargs: object) -> None:
        raise GitMutationBlocked("E2 exposes no Git mutation operation")
