from pathlib import Path


def preferred_env_path(root: Path) -> Path:
    """Return the preferred env path: .private/telegram.env if present, else .tmp/telegram.env."""
    # Allow an external override so secrets may live outside the repo
    from os import environ
    ext = environ.get('PRIVATE_ENV_PATH')
    if ext:
        p = Path(ext)
        if p.exists():
            return p

    private = root / '.private' / 'telegram.env'
    tmp = root / '.tmp' / 'telegram.env'
    return private if private.exists() else tmp


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def load_preferred_env(root: Path) -> dict:
    return load_env(preferred_env_path(root))
