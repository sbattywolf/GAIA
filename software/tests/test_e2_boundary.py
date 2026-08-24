from pathlib import Path

import pytest

from e2_engineer.boundary import (
    EngineerWorkspace,
    GitMutationBlocked,
    ProtectedPathBlocked,
    RunTestsPolicy,
    SecretPathBlocked,
    WorkspaceEscapeBlocked,
)


def workspace(tmp_path: Path) -> EngineerWorkspace:
    (tmp_path / "src").mkdir()
    (tmp_path / "protected").mkdir()
    (tmp_path / ".config" / "gaia").mkdir(parents=True)
    (tmp_path / ".config" / "gaia" / ".secrets.env").write_text("TOKEN=secret\n")
    return EngineerWorkspace(
        tmp_path,
        protected_paths=("protected", "ADR-0001-Core-Boundary.md"),
        sensitive_paths=(".config/gaia/.secrets.env", ".ssh"),
    )


def test_e2_t01_repository_read(tmp_path: Path):
    ws = workspace(tmp_path)
    (tmp_path / "src" / "example.py").write_text("answer = 42\n")
    assert ws.read_file("src/example.py") == "answer = 42\n"


def test_e2_t02_repository_search(tmp_path: Path):
    ws = workspace(tmp_path)
    (tmp_path / "src" / "example.py").write_text("def target():\n    return 42\n")
    assert ws.search(r"def target") == [("src/example.py", 1, "def target():")]


def test_e2_t03_bounded_write(tmp_path: Path):
    ws = workspace(tmp_path)
    ws.write_file("src/example.py", "answer = 43\n")
    assert (tmp_path / "src" / "example.py").read_text() == "answer = 43\n"


def test_e2_t04_workspace_escape_blocked(tmp_path: Path):
    ws = workspace(tmp_path)
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.read_file("../outside.txt")
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.write_file("/tmp/outside.txt", "nope")


def test_e2_t05_protected_path_blocked(tmp_path: Path):
    ws = workspace(tmp_path)
    with pytest.raises(ProtectedPathBlocked):
        ws.write_file("protected/file.txt", "nope")
    with pytest.raises(ProtectedPathBlocked):
        ws.write_file("ADR-0001-Core-Boundary.md", "nope")


def test_e2_t06_run_tests_is_bounded(tmp_path: Path):
    ws = workspace(tmp_path)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_smoke.py").write_text("def test_smoke():\n    assert True\n")
    result = ws.run_tests(["python", "-m", "pytest", "tests"], timeout=60)
    assert result.returncode == 0
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.run_tests(["python", "-m", "pytest", "/tmp/outside-tests"])


def test_e2_t07_diff_evidence(tmp_path: Path):
    ws = workspace(tmp_path)
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "example.txt").write_text("before\n")
    subprocess.run(["git", "add", "example.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=E2", "-c", "user.email=e2@example.invalid", "commit", "-qm", "baseline"], cwd=tmp_path, check=True)
    ws.write_file("example.txt", "after\n")
    result = ws.git_inspect(["diff", "--", "example.txt"])
    assert result.returncode == 0
    assert "after" in result.stdout


def test_e2_t08_git_mutation_blocked(tmp_path: Path):
    ws = workspace(tmp_path)
    for op in ("commit", "push", "merge", "reset"):
        with pytest.raises(GitMutationBlocked):
            ws.git_inspect([op])
    with pytest.raises(GitMutationBlocked):
        ws.git_mutate("commit")


def test_e2_t09_secret_hygiene(tmp_path: Path):
    ws = workspace(tmp_path)
    with pytest.raises(SecretPathBlocked):
        ws.read_file(".config/gaia/.secrets.env")
    with pytest.raises(SecretPathBlocked):
        ws.write_file(".config/gaia/.secrets.env", "TOKEN=bad\n")


def test_e2_t10_stop_condition_is_boundary_violation(tmp_path: Path):
    ws = workspace(tmp_path)
    with pytest.raises(GitMutationBlocked):
        ws.git_inspect(["branch", "--delete", "main"])


def test_run_tests_rejects_shell_operators():
    policy = RunTestsPolicy()
    with pytest.raises(Exception):
        policy.validate(["python", "-m", "pytest", "tests", "&&", "rm", "-rf", "."])


def _git_repo(tmp_path: Path) -> EngineerWorkspace:
    ws = workspace(tmp_path)
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "src" / "example.py").write_text("answer = 42\n")
    subprocess.run(["git", "add", "src/example.py"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=E2", "-c", "user.email=e2@example.invalid", "commit", "-qm", "baseline"],
        cwd=tmp_path,
        check=True,
    )
    return ws


def test_git_inspect_rejects_absolute_path_escape(tmp_path: Path):
    ws = _git_repo(tmp_path)
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.git_inspect(["diff", "--", "/tmp/outside.txt"])


def test_git_inspect_rejects_parent_traversal(tmp_path: Path):
    ws = _git_repo(tmp_path)
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.git_inspect(["diff", "--", "../outside.txt"])


def test_git_inspect_rejects_symlink_escape(tmp_path: Path):
    ws = _git_repo(tmp_path)
    outside = tmp_path.parent / "e2-outside-secret.txt"
    outside.write_text("secret\n")
    link = tmp_path / "src" / "outside-link"
    link.symlink_to(outside)
    with pytest.raises(WorkspaceEscapeBlocked):
        ws.git_inspect(["diff", "--", "src/outside-link"])


def test_git_inspect_valid_in_workspace_path_still_works(tmp_path: Path):
    ws = _git_repo(tmp_path)
    (tmp_path / "src" / "example.py").write_text("answer = 43\n")
    result = ws.git_inspect(["diff", "--", "src/example.py"])
    assert result.returncode == 0
    assert "answer = 43" in result.stdout


def test_git_inspect_rejects_sensitive_path(tmp_path: Path):
    ws = _git_repo(tmp_path)
    with pytest.raises(SecretPathBlocked):
        ws.git_inspect(["diff", "--", ".config/gaia/.secrets.env"])


@pytest.mark.parametrize(
    "args",
    [
        ["python", "-m", "pytest", "tests"],
        ["pytest", "tests"],
        ["python", "-m", "pytest", "-q", "tests"],
    ],
)
def test_run_tests_accepts_minimum_authorized_invocations(args):
    assert RunTestsPolicy().validate(args) == tuple(args)


@pytest.mark.parametrize(
    "args",
    [
        ["python", "-m", "pytest", "--confcutdir=/tmp", "tests"],
        ["python", "-m", "pytest", "-c", "/tmp/pytest.ini", "tests"],
        ["python", "-m", "pytest", "-p", "some_plugin", "tests"],
        ["python", "-m", "pytest", "--trace-config", "tests"],
        ["python", "-m", "pytest", "--import-mode=importlib", "tests"],
        ["python", "-m", "pytest", "--rootdir=/tmp", "tests"],
        ["python", "-m", "pytest", "--basetemp=/tmp", "tests"],
        ["python", "-m", "pytest", "--override-ini", "x=y", "tests"],
        ["python", "-m", "pytest", "--capture=tee-sys", "tests"],
        ["python", "-m", "pytest", "--disable-plugin-autoload", "tests"],
        ["python", "-m", "pytest", "--pyargs", "tests"],
        ["python", "-m", "pytest", "-o", "x=y", "tests"],
        ["python", "-m", "pytest", "--maxfail=0", "tests"],
    ],
)
def test_run_tests_rejects_configuration_plugin_import_environment_escape(args):
    with pytest.raises(Exception):
        RunTestsPolicy().validate(args)
