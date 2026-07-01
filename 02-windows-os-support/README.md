# 🪟 Windows 11 OS Support & Administration Lab

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L1-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project covers the day-to-day Windows OS administration tasks an L1 support engineer is expected to perform without escalation — process management, event log analysis, service recovery, local user management, and safe mode recovery — all practiced hands-on inside a Windows 11 Pro VM.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Windows 11 Pro | Client Workstation | `192.168.100.20` |

**Hypervisor:** VMware Workstation Pro

## 🎯 Objectives

- Identify and terminate a runaway process consuming excessive CPU/RAM
- Read and filter Windows Event Viewer logs for application and system errors
- Restart a stopped critical service (Print Spooler) and confirm recovery
- Create a local user account and a test scenario for password policy
- Boot into Safe Mode and back out, simulating a "PC won't start normally" ticket
- Pull full system info for hardware/software inventory documentation

## 🔧 Tools & Commands Used

`Task Manager` `Event Viewer (eventvwr)` `services.msc` `lusrmgr.msc` `msinfo32` `systeminfo` `wmic`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Task Manager: Identify & End High-Resource Process

Opened Task Manager and sorted by CPU and Memory columns to identify the heaviest process, simulating a "my PC is slow" ticket.

```
Ctrl + Shift + Esc → Processes tab → Click "CPU" column header to sort
```

📸 *Screenshot: `01-task-manager-sorted-by-cpu.png`*

---

### Step 2 — Event Viewer: Filter Application Errors

Navigated to Event Viewer and filtered the Application log for Error-level events from the last 24 hours — the standard first step when a user reports "my program keeps crashing."

```
Win + R → eventvwr → Windows Logs → Application → Filter Current Log → Level: Error
```

📸 *Screenshot: `02-event-viewer-application-errors.png`*

---

### Step 3 — Services: Restart a Stopped Critical Service

Stopped and then restarted the Print Spooler service to simulate resolving a "can't print" ticket — one of the most common L1 calls in any office environment.

```
Win + R → services.msc → Print Spooler → Right-click → Restart
```

📸 *Screenshot: `03-services-print-spooler-restart.png`*

---

### Step 4 — Local User Creation

Created a new local user account to simulate onboarding a new employee on a non-domain machine.

```
Win + R → lusrmgr.msc → Users → Right-click → New User
Username: testuser
Password: Test@12345
```

📸 *Screenshot: `04-local-user-account-created.png`*

---

### Step 5 — Safe Mode Boot & Recovery

Booted the machine into Safe Mode with Networking to simulate diagnosing a machine that won't boot normally — a frequent L1→L2 escalation point.

```
Settings → System → Recovery → Advanced Startup → Restart Now
→ Troubleshoot → Advanced Options → Startup Settings → Restart → Press 5
```

📸 *Screenshot: `05-safe-mode-boot-confirmation.png`*

---

### Step 6 — System Information Collection

Pulled full hardware/OS inventory for asset documentation, a standard requirement when handing off a ticket or logging a new device.

```cmd
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"Total Physical Memory"
```

📸 *Screenshot: `06-systeminfo-output.png`*

---

## ✅ Resolution Summary

| Task | Action Taken | Outcome |
|---|---|---|
| High CPU usage complaint | Identified runaway process via Task Manager | Process ended, CPU usage normalized |
| Printing not working | Restarted Print Spooler service | Print queue cleared, printing restored |
| New employee onboarding | Created local user account | Account ready for first login |
| PC not booting normally | Booted into Safe Mode | Confirmed OS loads — pointed to a driver/startup app conflict, not hardware failure |

## 📚 What This Demonstrates

- Confidence navigating core Windows administrative consoles without GUI hand-holding
- Ability to triage "vague" user complaints into a specific, actionable diagnosis
- Understanding of when a problem is software-level vs requires deeper (L2) intervention

## 🗂️ Folder Structure

```
02-windows-os-support/
├── README.md
└── screenshots/
    ├── 01-task-manager-sorted-by-cpu.png
    ├── 02-event-viewer-application-errors.png
    ├── 03-services-print-spooler-restart.png
    ├── 04-local-user-account-created.png
    ├── 05-safe-mode-boot-confirmation.png
    └── 06-systeminfo-output.png
```

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
