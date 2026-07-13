# SIEM Log Analysis Tool — L3 Practical Lab

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![Level](https://img.shields.io/badge/Level-L3%20IT%20Support-7B2FBE?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows%20Server-1a1a2e?style=for-the-badge)

> Python-based SIEM (Security Information and Event Management) log parser and analyzer. Parses Windows Event Logs, Linux syslogs, and generates threat intelligence dashboards.

---

## Overview

This tool simulates what enterprise SIEM tools like Splunk, QRadar, and Wazuh do internally — parse logs, correlate events, detect anomalies, and generate alerts.

**VM Setup Used:**
- Windows Server 2019: `192.168.100.10` — Log source (Windows Events)
- Windows 11 Client: `192.168.100.102` — Log source (endpoint events)
- Kali Linux: `192.168.100.20` — Run the SIEM tool + receive forwarded logs

**What you will learn:**
- Log parsing and correlation
- Windows Event ID reference and interpretation
- Linux syslog analysis
- Anomaly detection (failed logins, unusual hours)
- Alert generation and reporting
- Log forwarding setup (Windows to Kali)

---

## Key Windows Event IDs Reference

| Event ID | Description | Why It Matters |
|----------|-------------|----------------|
| 4624 | Successful logon | Track who logged in and when |
| 4625 | Failed logon | Detect brute force attempts |
| 4634 | Logoff | Track session durations |
| 4648 | Logon with explicit credentials | Detect pass-the-hash attacks |
| 4672 | Special privileges assigned | Admin logon tracking |
| 4720 | User account created | Detect unauthorized account creation |
| 4722 | User account enabled | Account lifecycle tracking |
| 4723 | Password change attempt | Monitor password changes |
| 4724 | Password reset by admin | Track admin resets |
| 4725 | User account disabled | Offboarding verification |
| 4728 | User added to global group | Detect privilege escalation |
| 4732 | User added to local group | Detect local admin additions |
| 4740 | Account locked out | Detect brute force or config issue |
| 4756 | User added to universal group | Group membership change |
| 4768 | Kerberos ticket requested | Authentication tracking |
| 4776 | NTLM authentication | Legacy auth detection |
| 7045 | New service installed | Detect malware persistence |
| 4688 | New process created | Process execution tracking |
| 4663 | File access attempt | Data access auditing |
| 1102 | Audit log cleared | Anti-forensics detection |

---

## Prerequisites

### On Kali Linux (192.168.100.20)

```bash
# Step 1: Open Terminal

# Step 2: Install Python dependencies
sudo apt update
pip3 install colorama tabulate python-dateutil watchdog

# Step 3: Install rsyslog for log receiving
sudo apt install rsyslog -y
sudo systemctl enable rsyslog
sudo systemctl start rsyslog

# Step 4: Verify rsyslog is running
sudo systemctl status rsyslog
# Expected: active (running)
```

### On Windows Server 2019 (192.168.100.10)

```powershell
# Step 1: Enable detailed audit logging
# Open Local Group Policy Editor (gpedit.msc) or run PowerShell:

# Enable logon/logoff auditing
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Logoff" /success:enable
auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable

# Verify audit policy is set
auditpol /get /category:*
# Should show Enabled next to each subcategory you set

# Step 2: Install NXLog for log forwarding to Kali Linux
# Download NXLog Community Edition from: https://nxlog.co/products/nxlog-community-edition/download
# Install with default settings

# Step 3: Configure NXLog to forward to Kali
# Edit file: C:\Program Files (x86)\nxlog\conf\nxlog.conf
# Add these lines:

<Output out>
    Module om_udp
    Host 192.168.100.20
    Port 514
</Output>

<Route 1>
    Path eventlog => out
</Route>
```

---

## Installation

### Step 1: Clone Repository on Kali Linux

```bash
git clone https://github.com/rithika-ujjalsingh/SIEM-Log-Analysis-Tool.git
cd SIEM-Log-Analysis-Tool
```

### Step 2: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 3: Configure the Tool

```bash
# Copy default config
cp config/config.example.json config/config.json

# Edit config
nano config/config.json

# Set these values:
# {
#   "log_sources": {
#     "windows_server": "192.168.100.10",
#     "windows_client": "192.168.100.102"
#   },
#   "alert_thresholds": {
#     "failed_logins": 5,
#     "lockouts_per_hour": 3,
#     "new_admin_accounts": 1
#   },
#   "business_hours": {
#     "start": "08:00",
#     "end": "19:00"
#   }
# }
```

### Step 4: Run the Analyzer

```bash
# Analyze a sample log file
python3 siem_analyzer.py --file sample_logs/windows_events.evtx

# Monitor live syslog (forwarded from Windows)
python3 siem_analyzer.py --live --port 514

# Generate HTML dashboard
python3 siem_analyzer.py --file sample_logs/windows_events.evtx --report html

# Expected output:
# =========================================
#   RIVI SIEM Log Analyzer v1.0
# =========================================
# Parsing log file: windows_events.evtx
# Events parsed: 1,247
#
# ALERTS:
# [HIGH] 47 failed logins for user john.doe in past hour
# [HIGH] Account lockout: john.doe locked 3 times today
# [MEDIUM] Login outside business hours: jane.smith at 02:34 AM
# [LOW] New user account created: temp.user at 11:45 PM
#
# Report saved: siem_report_20250701.html
```

---

## Usage Guide

### Analyze Windows Event Log Export

```bash
# Step 1: Export event log from Windows Server
# On Windows Server, open Event Viewer
# Right-click Security log → Save All Events As
# Save as: security_events.evtx
# Copy file to Kali: scp Administrator@192.168.100.10:C:\security_events.evtx /home/kali/

# Step 2: Analyze the exported log
python3 siem_analyzer.py --file security_events.evtx --format evtx

# Step 3: Filter for specific event IDs
python3 siem_analyzer.py --file security_events.evtx --event-ids 4625,4740,4720

# Step 4: Look for events in a specific time range
python3 siem_analyzer.py --file security_events.evtx \
    --start "2025-07-01 08:00" \
    --end "2025-07-01 18:00"
```

### Live Log Monitoring

```bash
# Step 1: Start the SIEM in live monitoring mode
# This listens on UDP port 514 for syslog from Windows
sudo python3 siem_analyzer.py --live --port 514

# Step 2: The tool will display alerts in real time:
# [2025-07-01 09:15:33] INFO  - Logon: john.doe from 192.168.100.102
# [2025-07-01 09:16:01] WARN  - Failed logon #3: john.doe from 192.168.100.102
# [2025-07-01 09:16:45] HIGH  - Account LOCKED: john.doe - 5 failed attempts
# [2025-07-01 09:16:46] HIGH  - ALERT: Possible brute force from 192.168.100.102

# Step 3: Press Ctrl+C to stop monitoring
# Step 4: Report is auto-saved on exit
```

### Generate Threat Report

```bash
# Generate full HTML report from analyzed logs
python3 siem_analyzer.py --file security_events.evtx --report html --output my_report.html

# Open in browser
# On Kali: firefox my_report.html
```

---

## Lab Exercises

### Exercise 1: Parse Sample Log File (20 minutes)

```
Sample log files are included in the sample_logs/ folder.

Step 1: Run analyzer on the included sample
  python3 siem_analyzer.py --file sample_logs/sample_windows.txt

Step 2: Count the events found by category
  How many successful logins?
  How many failed logins?
  Any account lockouts?
  Any new accounts created?

Step 3: Identify any suspicious patterns
  Are there logins outside business hours?
  Are there too many failed logins for one user?
  Are there any admin account changes?

Step 4: Generate the HTML report
  python3 siem_analyzer.py --file sample_logs/sample_windows.txt --report html

Step 5: Open the report in your browser and document your findings
```

### Exercise 2: Create Synthetic Attack Logs (25 minutes)

```
This exercise creates fake log entries simulating an attack.
You will then use the SIEM tool to detect the attack.

Step 1: Generate attack scenario logs
  python3 generate_test_logs.py --scenario brute_force --output attack_logs.txt

  This creates log entries showing:
  - 50 failed login attempts for user john.doe
  - All from IP 192.168.100.20 (Kali Linux)
  - Over a 10-minute period
  - Followed by account lockout

Step 2: Analyze the generated attack logs
  python3 siem_analyzer.py --file attack_logs.txt

Step 3: Verify the SIEM detected:
  [HIGH] Brute force alert for john.doe
  [HIGH] Account lockout: john.doe
  [HIGH] Source IP flagged: 192.168.100.20

Step 4: Write an incident summary based on what the SIEM found
  Who was targeted?
  What IP was the source?
  When did it happen?
  What was the impact?
```

### Exercise 3: Set Up Log Forwarding from Windows to Kali (30 minutes)

```
Step 1: On Kali Linux, configure rsyslog to receive logs
  sudo nano /etc/rsyslog.conf
  Uncomment these two lines:
    module(load="imudp")
    input(type="imudp" port="514")
  Save and exit

Step 2: Restart rsyslog
  sudo systemctl restart rsyslog

Step 3: Verify port 514 is open
  sudo ss -ulnp | grep 514
  Expected: Shows port 514 listening

Step 4: On Windows Server, install and configure NXLog
  Download NXLog Community Edition
  Install with default options
  Edit C:\Program Files (x86)\nxlog\conf\nxlog.conf
  Add UDP forwarding to 192.168.100.20 port 514

Step 5: Restart NXLog service
  On Windows Server:
  net stop nxlog
  net start nxlog

Step 6: Verify logs arriving on Kali
  sudo tail -f /var/log/syslog
  Then on Windows: log in and out
  You should see new entries in the Kali syslog

Step 7: Run SIEM in live mode
  sudo python3 siem_analyzer.py --live --port 514
  Perform some actions on Windows and watch events appear
```

---

## Alert Rules Reference

| Rule Name | Trigger | Severity |
|-----------|---------|----------|
| Brute Force Detection | More than 5 failed logins for same user in 10 min | HIGH |
| Account Lockout | Event ID 4740 detected | HIGH |
| After Hours Login | Successful login outside 08:00 to 19:00 | MEDIUM |
| New Admin Account | Event ID 4720 + added to Administrators group | HIGH |
| Audit Log Cleared | Event ID 1102 detected | CRITICAL |
| New Service Installed | Event ID 7045 detected | MEDIUM |
| Mass File Access | More than 100 Event ID 4663 in 5 minutes | HIGH |
| Multiple Account Lockouts | More than 3 lockouts in 1 hour | HIGH |

---

## Project Structure

```
SIEM-Log-Analysis-Tool/
|
├── siem_analyzer.py           Main SIEM engine
├── log_parser.py              Log format parsers
├── alert_engine.py            Alert rule detection
├── report_generator.py        HTML and CSV report builder
├── generate_test_logs.py      Synthetic log generator for labs
├── requirements.txt           Python dependencies
├── config/
│   ├── config.example.json    Sample configuration
│   └── alert_rules.json       Alert rule definitions
├── sample_logs/
│   ├── sample_windows.txt     Sample Windows events for practice
│   └── sample_linux.txt       Sample Linux syslog for practice
├── README.md                  This documentation file
├── SECURITY.md                Security policy
└── CONTRIBUTING.md            Contribution guidelines
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithika-u](https://linkedin.com/in/rithika-u)

*Built for IT Support learners | RIVI Enterprises 2025*
