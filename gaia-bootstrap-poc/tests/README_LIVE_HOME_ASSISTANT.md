# Live Home Assistant test configuration

The live integration test consumes configuration from outside the repository.

Expected files:

```text
~/.config/gaia/home_assistant.env
~/.config/gaia/.secrets.env
```

Required variables:

```text
HOME_ASSISTANT_BASE_URL
HOME_ASSISTANT_TOKEN
GAIA_HA_ENTITY_ID
```

The launcher maps the legacy-compatible names to the names expected by the
existing opt-in live test:

```text
HOME_ASSISTANT_BASE_URL -> GAIA_HA_URL
HOME_ASSISTANT_TOKEN    -> GAIA_HA_TOKEN
GAIA_HA_ENTITY_ID       -> GAIA_HA_ENTITY_ID
```

No credential, private URL, or entity value is stored in the repository.

The launcher exits before pytest if either external configuration file is
missing or any required variable is empty.

It deliberately does not load or forward unrelated legacy variables such as
Telegram, Ollama, OpenWebUI, Linear, or Zeus job/tool credentials.

Run it from the repository root:

```bash
./gaia-bootstrap-poc/scripts/run_live_home_assistant_test.sh
```

The test remains opt-in and performs one read-only request for one already
selected entity.

Do not commit either external configuration file to GAIA.
