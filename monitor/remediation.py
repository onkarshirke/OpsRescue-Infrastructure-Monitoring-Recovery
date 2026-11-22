#!/usr/bin/env python3
"""remediation.py - automatically recover a failed container and verify it."""

import subprocess
import time
import checks

def restart_container(name=checks.CONTAINER_NAME):
    """Attempt to restart the container. Returns True if the command succeeded."""
    try:
        result = subprocess.run(
            ['docker', 'restart', name],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False

def remediate(name=checks.CONTAINER_NAME, retries=3, wait=3):
    """Restart the container, then verify recovery by re-checking the website.
    Returns True if the service recovered, False if it needs escalation."""
    print(f"[REMEDIATION] {name} is DOWN - attempting automatic restart...")
    restart_container(name)

    for attempt in range(1, retries + 1):
        time.sleep(wait)
        if checks.website_up():
            print(f"[REMEDIATION] Recovery verified on attempt {attempt}. RESOLVED.")
            return True
        print(f"[REMEDIATION] Not back yet (attempt {attempt}/{retries}), waiting...")

    print(f"[REMEDIATION] {name} still down after {retries} attempts. ESCALATE.")
    return False
