from pathlib import Path


def test_live_launcher_uses_external_configuration_only():
    launcher = Path(__file__).parents[1] / "scripts" / "run_live_home_assistant_test.sh"
    text = launcher.read_text(encoding="utf-8")

    assert "$HOME/.config/gaia" in text
    assert ".secrets.env" in text
    assert "HOME_ASSISTANT_BASE_URL" in text
    assert "HOME_ASSISTANT_TOKEN" in text
    assert "GAIA_HA_ENTITY_ID" in text

    # No literal credential/config values belong in the launcher.
    assert "http://" not in text
    assert "https://" not in text
    assert "Bearer " not in text
