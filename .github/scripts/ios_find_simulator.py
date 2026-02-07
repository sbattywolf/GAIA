#!/usr/bin/env python3
import json
import subprocess
import sys
import uuid


def sh(args: list[str]) -> str:
    return subprocess.check_output(args, text=True).strip()


def main():
    # Prefer an already-created iPhone simulator if it exists.
    devices = json.loads(sh(["xcrun", "simctl", "list", "devices", "-j"]))
    candidates: list[tuple[str, str]] = []
    for runtime, devs in (devices.get("devices") or {}).items():
        for dev in devs or []:
            if not dev.get("isAvailable"):
                continue
            name = str(dev.get("name") or "")
            udid = str(dev.get("udid") or "")
            if not udid or not name.startswith("iPhone"):
                continue
            candidates.append((name, udid))

    candidates.sort(key=lambda it: (0 if "iPhone 16" in it[0] else 1, it[0]))
    if candidates:
        print(candidates[0][1])
        return

    # Otherwise, create one from the newest available iOS runtime.
    runtimes = json.loads(sh(["xcrun", "simctl", "list", "runtimes", "-j"])) .get("runtimes") or []
    ios = [rt for rt in runtimes if rt.get("platform") == "iOS" and rt.get("isAvailable")]
    if not ios:
        print("No available iOS runtimes found.", file=sys.stderr)
        sys.exit(1)


def version_key(rt: dict) -> tuple[int, ...]:
    parts: list[int] = []
    for p in str(rt.get("version") or "0").split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def create_simulator(device_type_id: str, runtime_id: str) -> str:
    return subprocess.check_output(["xcrun", "simctl", "create", f"CI iPhone {uuid.uuid4().hex[:8]}", device_type_id, runtime_id], text=True).strip()


if __name__ == '__main__':
    # reuse main logic but need access to version_key and create
    # find the best runtime and device and create simulator
    # Slightly reorganized compared to inline version to reuse functions
    try:
        devices = json.loads(subprocess.check_output(["xcrun", "simctl", "list", "devices", "-j"], text=True))
    except Exception:
        devices = {}
    candidates: list[tuple[str, str]] = []
    for runtime, devs in (devices.get("devices") or {}).items():
        for dev in devs or []:
            if not dev.get("isAvailable"):
                continue
            name = str(dev.get("name") or "")
            udid = str(dev.get("udid") or "")
            if not udid or not name.startswith("iPhone"):
                continue
            candidates.append((name, udid))

    candidates.sort(key=lambda it: (0 if "iPhone 16" in it[0] else 1, it[0]))
    if candidates:
        print(candidates[0][1])
        sys.exit(0)

    try:
        runtimes = json.loads(subprocess.check_output(["xcrun", "simctl", "list", "runtimes", "-j"], text=True)).get("runtimes") or []
    except Exception:
        runtimes = []
    ios = [rt for rt in runtimes if rt.get("platform") == "iOS" and rt.get("isAvailable")]
    if not ios:
        print("No available iOS runtimes found.", file=sys.stderr)
        sys.exit(1)

    ios.sort(key=version_key, reverse=True)
    runtime = ios[0]
    runtime_id = str(runtime.get("identifier") or "")
    if not runtime_id:
        print("Missing iOS runtime identifier.", file=sys.stderr)
        sys.exit(1)

    supported = runtime.get("supportedDeviceTypes") or []
    iphones = [dt for dt in supported if dt.get("productFamily") == "iPhone"]
    if not iphones:
        print("No iPhone device types for iOS runtime.", file=sys.stderr)
        sys.exit(1)

    iphones.sort(key=lambda dt: (0 if "iPhone 16" in str(dt.get("name") or "") else 1, str(dt.get("name") or "")))
    device_type_id = str(iphones[0].get("identifier") or "")
    if not device_type_id:
        print("Missing iPhone device type identifier.", file=sys.stderr)
        sys.exit(1)

    try:
        udid = create_simulator(device_type_id, runtime_id)
    except Exception:
        print("Failed to create iPhone simulator.", file=sys.stderr)
        sys.exit(1)
    print(udid)
