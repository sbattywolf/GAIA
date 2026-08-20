from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "scripts" / "pm002_start.sh"
STOP = ROOT / "scripts" / "pm002_stop.sh"
ROLLBACK = ROOT / "scripts" / "pm002_rollback.sh"

def test_pm2_t03_startup_fails_closed_when_external_config_is_missing(tmp_path):
    env = {"HOME": str(tmp_path), "GAIA_PM002_STATE_DIR": str(tmp_path / "state")}
    result = subprocess.run([str(START)], cwd=ROOT, env=env, text=True, capture_output=True)
    assert result.returncode != 0
    assert "Missing" in result.stderr

def test_pm2_t09_disabled_startup_never_attempts_external_read(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    (state / "disabled").write_text("disabled\n")
    env = {"HOME": str(tmp_path), "GAIA_PM002_STATE_DIR": str(state)}
    result = subprocess.run([str(START)], cwd=ROOT, env=env, text=True, capture_output=True)
    assert result.returncode == 3
    assert "disabled" in result.stderr.lower()

def test_pm2_t13_rollback_restores_enabled_local_state(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    (state / "disabled").write_text("disabled\n")
    env = {"HOME": str(tmp_path), "GAIA_PM002_STATE_DIR": str(state)}
    result = subprocess.run([str(ROLLBACK)], cwd=ROOT, env=env, text=True, capture_output=True)
    assert result.returncode == 0
    assert not (state / "disabled").exists()
    assert (state / "state").read_text().strip() == "enabled"

def test_pm2_t05_restart_procedure_is_stop_then_start_documented():
    text = Path("PM002_EVIDENCE.md").read_text()
    assert "restart" in text.lower()
    assert "pm002_stop.sh" in text
    assert "pm002_start.sh" in text
