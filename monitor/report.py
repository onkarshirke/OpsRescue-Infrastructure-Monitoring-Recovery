#!/usr/bin/env python3
"""report.py - generate an operational report from current metrics + incident history."""

from datetime import datetime
import checks
import database

def generate_report():
    """Build a full operational report as a string."""
    cpu, memory, disk = checks.get_metrics()
    container_up = checks.container_running()
    site_up = checks.website_up()
    incidents = database.get_all_incidents()

    total = len(incidents)
    resolved = sum(1 for i in incidents if i[4] == 'RESOLVED')
    escalated = sum(1 for i in incidents if i[4] == 'ESCALATED')
    recovery_rate = 100.0 if total == 0 else round(resolved / total * 100, 2)

    lines = []
    lines.append("=" * 50)
    lines.append("        INFRAWATCH - OPERATIONAL REPORT")
    lines.append("=" * 50)
    lines.append(f"  Generated:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("  CURRENT STATUS")
    lines.append("  " + "-" * 46)
    lines.append(f"  CPU usage:        {cpu}%")
    lines.append(f"  Memory usage:     {memory}%")
    lines.append(f"  Disk usage:       {disk}%")
    lines.append(f"  Web container:    {'UP' if container_up else 'DOWN'}")
    lines.append(f"  Website (8080):   {'UP' if site_up else 'DOWN'}")
    lines.append("")
    lines.append("  INCIDENT SUMMARY")
    lines.append("  " + "-" * 46)
    lines.append(f"  Total incidents:  {total}")
    lines.append(f"  Auto-resolved:    {resolved}")
    lines.append(f"  Escalated:        {escalated}")
    lines.append(f"  Recovery rate:    {recovery_rate}%")
    lines.append("")
    lines.append("  RECENT INCIDENTS")
    lines.append("  " + "-" * 46)
    if not incidents:
        lines.append("  (none recorded)")
    else:
        for ts, comp, sev, action, outcome in incidents[:5]:
            lines.append(f"  {ts}  {sev:8}  {comp} -> {outcome}")
    lines.append("=" * 50)

    return "\n".join(lines)

def save_report(text):
    """Write the report to a timestamped file in the logs folder."""
    filename = f"../logs/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(text)
    return filename

if __name__ == "__main__":
    report = generate_report()
    print(report)
    path = save_report(report)
    print(f"\n[SAVED] Report written to {path}")
