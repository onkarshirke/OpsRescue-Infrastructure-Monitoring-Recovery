#!/usr/bin/env python3
"""checks.py - all the health checks InfraWatch performs.
Every check is wrapped so it returns a value instead of ever crashing."""

import psutil
import subprocess
import urllib.request

CONTAINER_NAME = "infrawatch-web"
SERVICE_URL = "http://localhost:8080"

def get_metrics():
    """Return host CPU, memory and disk usage as percentages."""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk

def container_running(name=CONTAINER_NAME):
    """Return True if the named Docker container is currently running."""
    try:
        result = subprocess.run(
            ['docker', 'inspect', '-f', '{{.State.Running}}', name],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() == 'true'
    except Exception:
        return False

def website_up(url=SERVICE_URL):
    """Return True if the URL responds with HTTP 200."""
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return response.status == 200
    except Exception:
        return False
