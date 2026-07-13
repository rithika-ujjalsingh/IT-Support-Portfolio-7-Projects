#!/usr/bin/env python3
"""
SIEM Log Analysis Tool — L3 Practical Lab
Author: Rithika U | RIVI Enterprises
"""

import re
import sys
import json
import socket
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from colorama import init, Fore, Style

init(autoreset=True)

# ── Windows Event ID Reference ──────────────────────────────
EVENT_IDS = {
    4624: "Successful Logon",
    4625: "Failed Logon",
    4634: "Logoff",
    4648: "Logon with Explicit Credentials",
    4672: "Special Privileges Assigned",
    4720: "User Account Created",
    4722: "User Account Enabled",
    4723: "Password Change Attempt",
    4724: "Password Reset by Admin",
    4725: "User Account Disabled",
    4728: "User Added to Global Group",
    4732: "User Added to Local Group",
    4740: "Account Locked Out",
    4756: "User Added to Universal Group",
    7045: "New Service Installed",
    4688: "New Process Created",
    4663: "File Access Attempt",
    1102: "Audit Log Cleared",
}

BUSINESS_HOURS_START = 8   # 8 AM
BUSINESS_HOURS_END   = 19  # 7 PM

BRUTE_FORCE_THRESHOLD    = 5   # failed logins per user in window
BRUTE_FORCE_WINDOW_MINS  = 10  # minutes
LOCKOUT_ALERT_THRESHOLD  = 3   # lockouts per hour

class SIEMAnalyzer:
    def __init__(self):
        self.events      = []
        self.alerts      = []
        self.stats       = defaultdict(int)
        self.failed_logins_by_user = defaultdict(list)
        self.lockouts    = []

    def banner(self):
        print(Fore.CYAN + "=" * 50)
        print(Fore.GREEN + "  RIVI SIEM Log Analyzer v1.0")
        print(Fore.CYAN + "=" * 50)

    # ── Parsers ─────────────────────────────────────────────

    def parse_text_log(self, filepath):
        """Parse plain-text log with lines like: 2025-07-01 09:15:33 EventID=4625 User=john.doe IP=192.168.100.102"""
        print(Fore.YELLOW + f"[*] Parsing text log: {filepath}")
        parsed = 0
        with open(filepath, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                event = self._parse_text_line(line)
                if event:
                    self.events.append(event)
                    parsed += 1
        print(Fore.GREEN + f"[+] Parsed {parsed} events")

    def _parse_text_line(self, line):
        """Extract fields from a structured text log line."""
        event = {}
        # Timestamp: first two tokens (date + time)
        ts_match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", line)
        if ts_match:
            try:
                event["timestamp"] = datetime.strptime(
                    f"{ts_match.group(1)} {ts_match.group(2)}", "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                return None

        # Key=Value pairs
        for key, pattern in [
            ("event_id", r"EventID=(\d+)"),
            ("user",     r"User=([\w.\-@]+)"),
            ("ip",       r"IP=([\d.]+)"),
            ("message",  r"Msg=(.+)$"),
        ]:
            m = re.search(pattern, line)
            if m:
                event[key] = int(m.group(1)) if key == "event_id" else m.group(1)

        return event if "event_id" in event else None

    # ── Detection Rules ──────────────────────────────────────

    def run_detections(self):
        print(Fore.YELLOW + "\n[*] Running detection rules...")
        self._detect_brute_force()
        self._detect_lockouts()
        self._detect_after_hours()
        self._detect_new_accounts()
        self._detect_audit_cleared()
        self._tally_stats()

    def _detect_brute_force(self):
        window = timedelta(minutes=BRUTE_FORCE_WINDOW_MINS)
        # Collect all failed logins per user
        for ev in self.events:
            if ev.get("event_id") == 4625:
                user = ev.get("user", "unknown")
                ts   = ev.get("timestamp")
                if ts:
                    self.failed_logins_by_user[user].append(ts)

        for user, times in self.failed_logins_by_user.items():
            times.sort()
            # Sliding window check
            for i, t in enumerate(times):
                window_events = [x for x in times if t <= x <= t + window]
                if len(window_events) >= BRUTE_FORCE_THRESHOLD:
                    ip = next(
                        (ev.get("ip", "unknown") for ev in self.events
                         if ev.get("event_id") == 4625 and ev.get("user") == user),
                        "unknown"
                    )
                    self._add_alert(
                        "HIGH",
                        f"Brute force detected: {len(window_events)} failed logins for '{user}' "
                        f"in {BRUTE_FORCE_WINDOW_MINS} min window (source IP: {ip})"
                    )
                    break

    def _detect_lockouts(self):
        hour_ago = None
        for ev in self.events:
            if ev.get("event_id") == 4740:
                self.lockouts.append(ev)
                user = ev.get("user", "unknown")
                self._add_alert("HIGH", f"Account lockout detected: '{user}'")

        # Check for multiple lockouts per hour
        if len(self.lockouts) >= LOCKOUT_ALERT_THRESHOLD:
            self._add_alert(
                "HIGH",
                f"Multiple lockouts in session: {len(self.lockouts)} lockout events detected — "
                "possible active attack in progress"
            )

    def _detect_after_hours(self):
        for ev in self.events:
            if ev.get("event_id") == 4624:
                ts = ev.get("timestamp")
                user = ev.get("user", "unknown")
                if ts and (ts.hour < BUSINESS_HOURS_START or ts.hour >= BUSINESS_HOURS_END):
                    self._add_alert(
                        "MEDIUM",
                        f"After-hours login: '{user}' logged in at {ts.strftime('%H:%M')} "
                        f"(business hours: {BUSINESS_HOURS_START:02d}:00–{BUSINESS_HOURS_END:02d}:00)"
                    )

    def _detect_new_accounts(self):
        for ev in self.events:
            if ev.get("event_id") == 4720:
                user = ev.get("user", "unknown")
                ts   = ev.get("timestamp")
                ts_str = ts.strftime("%Y-%m-%d %H:%M") if ts else "unknown time"
                self._add_alert("HIGH", f"New user account created: '{user}' at {ts_str}")

    def _detect_audit_cleared(self):
        for ev in self.events:
            if ev.get("event_id") == 1102:
                ts = ev.get("timestamp")
                ts_str = ts.strftime("%Y-%m-%d %H:%M") if ts else "unknown time"
                self._add_alert(
                    "CRITICAL",
                    f"AUDIT LOG CLEARED at {ts_str} — potential anti-forensics activity!"
                )

    def _tally_stats(self):
        for ev in self.events:
            eid = ev.get("event_id")
            if eid:
                self.stats[eid] += 1

    def _add_alert(self, severity, message):
        self.alerts.append({"severity": severity, "message": message, "time": datetime.now()})

    # ── Reporting ────────────────────────────────────────────

    def print_report(self):
        print(Fore.CYAN + "\n" + "=" * 55)
        print(Fore.CYAN + "  SIEM ANALYSIS REPORT")
        print(Fore.CYAN + "=" * 55)

        print(Fore.WHITE + f"\nTotal events analyzed: {len(self.events)}")

        print(Fore.YELLOW + "\nEvent Summary:")
        for eid, count in sorted(self.stats.items()):
            label = EVENT_IDS.get(eid, "Unknown")
            print(f"  EventID {eid:5d}  [{label:35s}]  Count: {count}")

        print(Fore.RED + f"\nALERTS ({len(self.alerts)} total):")
        if not self.alerts:
            print(Fore.GREEN + "  No alerts generated — environment looks clean!")
        else:
            sev_color = {"CRITICAL": Fore.RED, "HIGH": Fore.RED,
                         "MEDIUM": Fore.YELLOW, "LOW": Fore.WHITE}
            for alert in self.alerts:
                color = sev_color.get(alert["severity"], Fore.WHITE)
                print(color + f"  [{alert['severity']:8s}] {alert['message']}")

    def save_report_html(self, output="siem_report.html"):
        rows = ""
        sev_badge = {"CRITICAL": "#FF0000", "HIGH": "#FF4500",
                     "MEDIUM": "#FFD700", "LOW": "#00FF41"}
        for a in self.alerts:
            color = sev_badge.get(a["severity"], "#ffffff")
            rows += f'<tr><td style="color:{color};font-weight:bold">{a["severity"]}</td><td>{a["message"]}</td></tr>\n'

        html = f"""<!DOCTYPE html>
<html>
<head>
<title>RIVI SIEM Report</title>
<style>
  body {{ background:#0a0a1a; color:#00FF41; font-family:'Courier New',monospace; padding:20px; }}
  h1 {{ color:#0096FF; }} h2 {{ color:#FFD700; }}
  table {{ border-collapse:collapse; width:100%; }}
  th {{ background:#1a1a2e; color:#0096FF; padding:10px; text-align:left; }}
  td {{ border:1px solid #333; padding:8px; }}
  tr:nth-child(even) {{ background:#111122; }}
  .stat {{ background:#111133; padding:10px; margin:5px; display:inline-block; border-radius:4px; }}
</style>
</head>
<body>
<h1>🛡 RIVI SIEM Security Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<div>
  <span class="stat">Total Events: <b>{len(self.events)}</b></span>
  <span class="stat">Alerts: <b style="color:#FF4500">{len(self.alerts)}</b></span>
  <span class="stat">Lockouts: <b style="color:#FF0000">{len(self.lockouts)}</b></span>
</div>
<h2>Alerts</h2>
<table>
  <tr><th>Severity</th><th>Description</th></tr>
  {rows if rows else '<tr><td colspan="2" style="color:#00FF41">No alerts — environment clean</td></tr>'}
</table>
<h2>Event ID Summary</h2>
<table>
  <tr><th>Event ID</th><th>Description</th><th>Count</th></tr>
  {''.join(f"<tr><td>{eid}</td><td>{EVENT_IDS.get(eid,'Unknown')}</td><td>{cnt}</td></tr>" for eid, cnt in sorted(self.stats.items()))}
</table>
<p style="color:#555;margin-top:30px">RIVI Enterprises | Cybersecurity Engineer: Rithika U</p>
</body>
</html>"""
        with open(output, "w") as f:
            f.write(html)
        print(Fore.GREEN + f"\n[+] HTML report saved: {output}")

    # ── Live Syslog Mode ─────────────────────────────────────

    def start_live(self, port=514):
        print(Fore.CYAN + f"\n[*] Listening for syslog on UDP port {port} ...")
        print(Fore.YELLOW + "Press Ctrl+C to stop\n")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", port))
        sev_color = {"CRITICAL": Fore.RED, "HIGH": Fore.RED,
                     "MEDIUM": Fore.YELLOW, "LOW": Fore.WHITE}
        try:
            while True:
                data, addr = sock.recvfrom(4096)
                line = data.decode("utf-8", errors="replace").strip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(Fore.CYAN + f"[{timestamp}]" + Fore.WHITE + f" {addr[0]}: " + line[:120])

                event = self._parse_text_line(line)
                if event:
                    self.events.append(event)
                    self.run_detections()
                    for alert in self.alerts[-1:]:  # show latest alert
                        color = sev_color.get(alert["severity"], Fore.WHITE)
                        print(color + f"  ⚠ ALERT [{alert['severity']}]: {alert['message']}")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n[*] Stopping live monitor...")
            self.print_report()

# ── CLI Entry Point ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RIVI SIEM Log Analyzer")
    parser.add_argument("--file",        help="Log file to analyze")
    parser.add_argument("--live",        action="store_true", help="Live syslog monitoring mode")
    parser.add_argument("--port",        type=int, default=514, help="UDP port for live mode")
    parser.add_argument("--report",      choices=["html", "text"], default="text")
    parser.add_argument("--output",      default="siem_report.html", help="Output file for HTML report")
    parser.add_argument("--event-ids",   help="Comma-separated Event IDs to filter (e.g. 4625,4740)")
    args = parser.parse_args()

    siem = SIEMAnalyzer()
    siem.banner()

    if args.live:
        siem.start_live(args.port)
        return

    if args.file:
        siem.parse_text_log(args.file)
        siem.run_detections()
        siem.print_report()
        if args.report == "html":
            siem.save_report_html(args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
