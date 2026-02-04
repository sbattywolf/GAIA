import os
import time
import subprocess
import shutil
import urllib.request
import pytest


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
        try:
            if os.environ.get("RUN_E2E", "0") == "1":
                # Start local mock only when using default URL and when RUN_E2E=1
                if mock_url.endswith("127.0.0.1:8001/health"):
                    cmd = [sys.executable, "scripts/mock_token_service.py", "--port", "8001"]
                    mock_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for mock service to become ready
    for _ in range(15):
        try:
            with urllib.request.urlopen(mock_url, timeout=3) as r:
                assert r.status == 200
                break
        except Exception:
            time.sleep(1)
    else:
        pytest.fail(f"mock service not ready at {mock_url}")
        finally:
            if mock_proc:
                mock_proc.terminate()
                try:
                    mock_proc.wait(timeout=5)
                except Exception:
                    mock_proc.kill()

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

    subprocess.run(cmd, check=True, env=env)
