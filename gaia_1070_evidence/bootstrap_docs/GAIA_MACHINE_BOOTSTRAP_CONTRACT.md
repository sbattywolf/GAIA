# GAIA MACHINE BOOTSTRAP CONTRACT

## Machine Identity:
    1070 (sbatta-1070-aiaiai)

## SSH Transport:
    gaia-1070 alias with key authentication

## OpenClaw Node Identity:
    Persistent device identity

## Runtime Role:
    Agent execution platform

## GPU/Model Profile:
    NVIDIA GeForce GTX 1070 Max-Q (8GB VRAM)

## Secrets:
    SSH keys outside Git, temporary pairing credentials

This contract is reusable for future machines such as Z and N, with machine-specific identity and hardware profile substituted as appropriate.

## Intended Lifecycle:

    one-time privileged bootstrap
        ↓
    persistent systemd/OpenClaw node
        ↓
    reboot
        ↓
    automatic node restart/reconnect

## Clarifications:

- SSH is the management/bootstrap plane
- OpenClaw Node is the operational machine/agent plane
- sudo is for one-time administrative setup only
- sudo passwords must never be stored in Git, .env or runtime config
- SSH private keys remain outside Git
- the 3090 Gateway token is NOT copied as a permanent 1070 credential