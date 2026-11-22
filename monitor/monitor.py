#!/usr/bin/env python3
"""monitor.py - InfraWatch main entry point."""

import checks
import remediation
import database

def show_health():
    cpu, memory, disk = checks.get_metrics()
    container_up = checks.container_running()
    site_up = checks.website_up()

    print("=" * 42)
    print("        INFRAWATCH - SYSTEM HEALTH")
    print("=" * 42)
    print(f"  CPU usage:        {cpu}%")
    print(f"  Memory usage:     {memory}%")
    print(f"  Disk usage:       {disk}%")
    print(f"  Web container:    {'UP' if container_up else 'DOWN'}")
    print(f"  Website (8080):   {'UP' if site_up else 'DOWN'}")
    print("=" * 42)

    return container_up, site_up

def run():
    database.init_db()
    container_up, site_up = show_health()

    if not container_up or not site_up:
        recovered = remediation.remediate()
        outcome = "RESOLVED" if recovered else "ESCALATED"
        database.log_incident(
            component="infrawatch-web",
            severity="CRITICAL",
            action="Automatic container restart",
            outcome=outcome
        )
        print(f"[LOGGED] Incident recorded with outcome: {outcome}")
    else:
        print("[OK] All services healthy. No action needed.")

if __name__ == "__main__":
    run()
