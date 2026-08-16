#!/usr/bin/env python3

import subprocess
import time
from datetime import datetime, timezone


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def gpu_snapshot():
    query = (
        "timestamp,"
        "utilization.gpu,"
        "memory.used,"
        "memory.total,"
        "temperature.gpu,"
        "power.draw"
    )

    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                f"--query-gpu={query}",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return {
                "available": False,
                "error": result.stderr.strip(),
            }

        line = result.stdout.strip().splitlines()[0]
        values = [v.strip() for v in line.split(",")]

        return {
            "available": True,
            "timestamp": values[0],
            "gpu_utilization_percent": _number(values[1]),
            "memory_used_mib": _number(values[2]),
            "memory_total_mib": _number(values[3]),
            "temperature_c": _number(values[4]),
            "power_draw_w": _number(values[5]),
        }

    except FileNotFoundError:
        return {
            "available": False,
            "error": "nvidia-smi not found",
        }

    except Exception as exc:
        return {
            "available": False,
            "error": str(exc),
        }


def cpu_ram_snapshot():
    try:
        import os

        load1, load5, load15 = os.getloadavg()

        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            meminfo = {}

            for line in f:
                key, value = line.split(":", 1)
                value = value.strip().split()[0]
                meminfo[key] = int(value)

        total = meminfo.get("MemTotal", 0)
        available = meminfo.get("MemAvailable", 0)
        used = total - available

        return {
            "available": True,
            "load_average": {
                "1m": load1,
                "5m": load5,
                "15m": load15,
            },
            "ram_total_mib": round(total / 1024, 2),
            "ram_available_mib": round(available / 1024, 2),
            "ram_used_mib": round(used / 1024, 2),
        }

    except Exception as exc:
        return {
            "available": False,
            "error": str(exc),
        }


def snapshot():
    return {
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "gpu": gpu_snapshot(),
        "cpu_ram": cpu_ram_snapshot(),
    }


def aggregate(samples):
    if not samples:
        return {}

    gpu_samples = [
        s["gpu"]
        for s in samples
        if s.get("gpu", {}).get("available")
    ]

    cpu_samples = [
        s["cpu_ram"]
        for s in samples
        if s.get("cpu_ram", {}).get("available")
    ]

    def values(items, key):
        return [
            x[key]
            for x in items
            if x.get(key) is not None
        ]

    gpu_util = values(
        gpu_samples,
        "gpu_utilization_percent",
    )

    gpu_mem = values(
        gpu_samples,
        "memory_used_mib",
    )

    gpu_temp = values(
        gpu_samples,
        "temperature_c",
    )

    power = values(
        gpu_samples,
        "power_draw_w",
    )

    ram = values(
        cpu_samples,
        "ram_used_mib",
    )

    return {
        "sample_count": len(samples),

        "gpu": {
            "utilization_avg_percent": (
                sum(gpu_util) / len(gpu_util)
                if gpu_util else None
            ),
            "utilization_peak_percent": (
                max(gpu_util)
                if gpu_util else None
            ),
            "memory_peak_mib": (
                max(gpu_mem)
                if gpu_mem else None
            ),
            "temperature_peak_c": (
                max(gpu_temp)
                if gpu_temp else None
            ),
            "power_peak_w": (
                max(power)
                if power else None
            ),
        },

        "cpu_ram": {
            "ram_peak_mib": (
                max(ram)
                if ram else None
            ),
        },
    }


class TelemetrySession:
    def __init__(self, interval_seconds=2.0):
        self.interval_seconds = interval_seconds
        self.samples = []
        self.running = False

    def start(self):
        self.running = True
        self.samples.append(snapshot())

    def sample(self):
        if self.running:
            self.samples.append(snapshot())

    def stop(self):
        if self.running:
            self.samples.append(snapshot())
            self.running = False

    def result(self):
        return {
            "samples": self.samples,
            "summary": aggregate(self.samples),
        }
