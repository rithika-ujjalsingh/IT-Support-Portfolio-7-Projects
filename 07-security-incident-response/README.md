# 🛡️ Security Incident Response — Brute-Force Detection & Containment

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L3-purple)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project simulates a realistic security incident — an SSH brute-force attack against a Windows client from an external host — and walks through the full incident response lifecycle: detection via log analysis, containment via account lockout policy and firewall rules, and documentation suitable for a post-incident report.

> ⚠️ **Lab-only disclaimer:** This attack was performed exclusively within an isolated VMware lab environment that I own and control, against my own VMs, for educational and skill-demonstration purposes only. No external systems were targeted.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Kali Linux | Simulated Attacker | `192.168.100.102` |
| Windows 11 Pro | Simulated Victim (SSH-enabled target) | `192.168.100.20` |
| Windows Server 2019 | Domain Controller (policy enforcement) | `192.168.100.10` |

**Hypervisor:** VMware Workstation Pro — isolated host-only network, no internet bridging

## 🎯 Objectives

- Simulate a brute-force login attempt against a target machine
- Detect the attack using Windows Security Event Logs (Event ID 4625)
- Contain the threat by enforcing an account lockout policy via GPO
- Block the attacking IP at the Windows Firewall level
- Document the full incident timeline in a format suitable for a SOC report

## 🔧 Tools & Commands Used

`hydra` `Event Viewer` `PowerShell (Get-WinEvent)` `Group Policy (Account Lockout Policy)` `Windows Defender Firewall (New-NetFirewallRule)`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Simulated Attack (Controlled Lab Only)

Ran a brute-force attempt from Kali against the Windows 11 target's SSH service to generate realistic failed-login telemetry.

```bash
hydra -l administrator -P /usr/share/wordlists/rockyou.txt ssh://192.168.100.20
```

📸 *Screenshot: `01-hydra-bruteforce-simulation.png`*

---

### Step 2 — Detection: Failed Login Events

Identified the attack pattern in Windows Security logs — a high volume of Event ID 4625 (failed logon) from a single source IP in a short window is the textbook brute-force signature.

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} |
  Select TimeCreated, @{N='User';E={$_.Properties[5].Value}},
    @{N='SourceIP';E={$_.Properties[19].Value}} |
  Sort TimeCreated -Descending | Select -First 20
```

📸 *Screenshot: `02-event-4625-failed-logons.png`*

---

### Step 3 — Containment: Account Lockout Policy

Configured a domain-wide lockout policy so repeated failed attempts automatically lock the account, stopping the attack from succeeding through sheer attempt volume.

```
GPMC → Account Lockout Policy
Account lockout threshold: 5 invalid attempts
Account lockout duration: 30 minutes
```

📸 *Screenshot: `03-account-lockout-policy-config.png`*

---

### Step 4 — Verify Lockout Triggered

```powershell
Search-ADAccount -LockedOut | Select Name, SamAccountName, LockedOut
```

📸 *Screenshot: `04-account-lockout-triggered.png`*

---

### Step 5 — Containment: Block Attacker IP at Firewall

```powershell
New-NetFirewallRule -DisplayName "Block Suspicious IP - Kali" `
  -Direction Inbound -RemoteAddress 192.168.100.102 `
  -Action Block -Protocol Any
```

📸 *Screenshot: `05-firewall-ip-block-rule.png`*

---

### Step 6 — Verify Containment

Confirmed the attacking host could no longer reach the target after the firewall rule was applied.

```bash
ping 192.168.100.20
```
*(Expected: Request timed out / 100% packet loss)*

📸 *Screenshot: `06-attacker-blocked-confirmation.png`*

---

## 📄 Incident Report Summary

| Field | Detail |
|---|---|
| **Incident Type** | SSH Brute-Force Attempt (simulated) |
| **Detection Method** | Windows Security Event Log — Event ID 4625 pattern analysis |
| **Source** | 192.168.100.102 (Kali Linux test host) |
| **Target** | 192.168.100.20 (Windows 11 client) |
| **Containment Actions** | 1) Account lockout policy (5 attempts / 30 min) 2) Source IP blocked at host firewall |
| **Time to Detect** | Immediate (logs reviewed in real time) |
| **Time to Contain** | Under 10 minutes from detection to both controls applied |
| **Residual Risk** | None — attacker IP fully blocked, account lockout active domain-wide |

## 📚 What This Demonstrates

- Full incident response lifecycle: simulate → detect → contain → verify → document
- Practical log analysis skills using native Windows tooling (no SIEM dependency)
- Defense-in-depth thinking — applying two independent controls (account policy + firewall) rather than relying on one
- Report-writing discipline matching what's expected in a real SOC handoff or post-incident review

## 🗂️ Folder Structure

```
07-security-incident-response/
├── README.md
└── screenshots/
    ├── 01-hydra-bruteforce-simulation.png
    ├── 02-event-4625-failed-logons.png
    ├── 03-account-lockout-policy-config.png
    ├── 04-account-lockout-triggered.png
    ├── 05-firewall-ip-block-rule.png
    └── 06-attacker-blocked-confirmation.png
```

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
