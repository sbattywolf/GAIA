import os
import time
import subprocess
import shutil
import urllib.request
import pytest
import sys


@pytest.mark.e2e
def test_mock_service_and_postgres_ready():
    """Checks mock token service health and a basic Postgres query via psql.

    This test is intentionally minimal to verify infrastructure readiness in CI.
    """
    # Only run E2E tests when explicitly enabled in CI (avoid running on regular integration jobs)
    if os.environ.get("RUN_E2E", "0") != "1":
        pytest.skip("E2E tests disabled (set RUN_E2E=1 to enable)")

    mock_url = os.environ.get("MOCK_URL", "http://127.0.0.1:8001/health")

    # If CI/workflow didn't start the mock, start it from the test to make this
    # check self-contained and OS-independent.
    mock_proc = None
    # Temporary debug info to aid intermittent flake triage
    print("[DEBUG] test_mock_service_and_postgres_ready starting")
    try:
        import platform
        print(f"[DEBUG] platform: {platform.platform()} python: {sys.executable}")
    except Exception:
        pass
    # Print selected environment variables that affect infra checks
    try:
        keys = [
            "RUN_E2E",
            "MOCK_URL",
            "PGHOST",
            "PGPORT",
            "PGUSER",
            "PGDATABASE",
            "PGPASSWORD",
        ]
        env_dump = {k: os.environ.get(k) for k in keys}
        print("[DEBUG] env:", env_dump)
    except Exception:
        pass
    if os.environ.get("RUN_E2E", "0") == "1":
        # Start local mock only when using the default local URL
        if mock_url.startswith("http://127.0.0.1"):
            cmd = [sys.executable, "scripts/mock_token_service.py", "--port", "8001"]
            mock_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for mock service to become ready
        start_wait = time.time()
        for _ in range(30):
            try:
                with urllib.request.urlopen(mock_url, timeout=3) as r:
                    assert r.status == 200
                    break
            except Exception:
                time.sleep(1)
        else:
            # Capture a last attempt response for debugging
            try:
                with urllib.request.urlopen(mock_url, timeout=3) as r:
                    print(f"[DEBUG] last_status={r.status}")
            except Exception as e:
                print(f"[DEBUG] mock_connect_error: {e}")
            pytest.fail(f"mock service not ready at {mock_url}")
        else:
            # If we broke early, print how long it took
            elapsed = time.time() - start_wait
            print(f"[DEBUG] mock_ready_elapsed={elapsed:.2f}s")
    finally:
        if mock_proc:
            try:
                mock_proc.terminate()
                mock_proc.wait(timeout=5)
            except Exception:
                try:
                    mock_proc.kill()
                except Exception:
                    pass
            # Attempt to surface any captured mock logs for CI debugging
            try:
                out, err = mock_proc.communicate(timeout=1)
                if out:
                    print("[DEBUG] mock stdout:\n", out.decode(errors="ignore"))
                if err:
                    print("[DEBUG] mock stderr:\n", err.decode(errors="ignore"))
            except Exception as e:
                print(f"[DEBUG] mock_communicate_error: {e}")

    # Check Postgres using psql if available
    if shutil.which("psql") is None:
        pytest.skip("psql not available in runner; skipping DB check")

    pg_host = os.environ.get("PGHOST", "127.0.0.1")
    pg_port = os.environ.get("PGPORT", "5432")
    pg_user = os.environ.get("PGUSER", "gaia_test")
    pg_db = os.environ.get("PGDATABASE", "gaia_test_db")
    pg_password = os.environ.get("PGPASSWORD", "gaia_test_pass")

    env = os.environ.copy()
    env["PGPASSWORD"] = pg_password

    cmd = [
        "psql",
        "-h",
        pg_host,
        "-p",
        str(pg_port),
        "-U",
        pg_user,
        "-d",
        pg_db,
        "-c",
        "SELECT 1;",
    ]

    # Run psql and capture output for richer debugging
    print(f"[DEBUG] invoking psql: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False, env=env, capture_output=True, text=True)
        print("[DEBUG] psql returncode:", result.returncode)
        if result.stdout:
            print("[DEBUG] psql stdout:\n" + result.stdout)
        if result.stderr:
            print("[DEBUG] psql stderr:\n" + result.stderr)
        if result.returncode != 0:
            pytest.fail(f"psql check failed (rc={result.returncode}). See stdout/stderr above")
    except Exception as e:
        # Attempt to capture process list to help triage platform-specific issues
        try:
            import platform
            if platform.system().lower().startswith("win"):
                proc = subprocess.run(["tasklist"], capture_output=True, text=True)
                print("[DEBUG] tasklist:\n" + proc.stdout)
            else:
                proc = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
                print("[DEBUG] ps -ef (truncated):\n" + '\n'.join(proc.stdout.splitlines()[:50]))
        except Exception:
            pass
        raise
    print("[DEBUG] psql check invoked (success)")
