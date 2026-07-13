# 🎫 IT Support Ticketing System — L1 Practical Lab

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![Level](https://img.shields.io/badge/Level-L1%20IT%20Support-00FF41?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20Kali%20Linux-1a1a2e?style=for-the-badge)

> A command-line IT Support Ticketing System simulating real helpdesk workflows. Built for L1 IT Support Engineers — ServiceNow-style ticket management via CLI.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation Step by Step](#installation)
- [Usage Guide](#usage-guide)
- [Lab Exercises](#lab-exercises)
- [Ticket Workflow](#ticket-workflow)
- [Escalation Rules](#escalation-rules)
- [Project Structure](#project-structure)

---

## Overview

This project simulates a real-world IT helpdesk ticketing system.

**VM Setup Used:**
- Windows 11 Client: `192.168.100.102`
- Windows Server 2019: `192.168.100.10`
- Kali Linux: `192.168.100.20`

**What you will learn:**
- Ticket creation with priority (P1 to P4) and category tagging
- Status tracking (Open to In Progress to Escalated to Resolved to Closed)
- SLA timer per priority level
- Escalation logic (L1 to L2 to L3)
- JSON-based local database

---

## Features

| Feature | Description |
|---------|-------------|
| Ticket CRUD | Create, Read, Update, Delete tickets |
| Priority Levels | P1 Critical to P4 Low with SLA timers |
| Categories | Hardware, Software, Network, Account, Security |
| Escalation | Auto-escalate based on time and severity |
| Dashboard | Live stats open/closed/escalated counts |
| Audit Log | Full history of every action taken |
| Search | Filter by status, priority, category, user |
| Export | CSV export for reporting |

---

## Prerequisites

### On Windows 11 VM (192.168.100.102)

```powershell
# Step 1: Open PowerShell as Administrator
# Right-click Start menu, select Windows PowerShell Admin

# Step 2: Check Python version
python --version
# Expected output: Python 3.10.x or higher

# Step 3: If Python not installed, download from python.org
# During install, check the box Add Python to PATH

# Step 4: Verify pip is working
pip --version
# Expected output: pip 23.x.x from C:\Users\...

# Step 5: Install Git
winget install Git.Git
# Press Y when prompted
```

### On Kali Linux VM (192.168.100.20)

```bash
# Step 1: Open Terminal with Ctrl+Alt+T

# Step 2: Update package list
sudo apt update
# Enter your password when prompted

# Step 3: Upgrade existing packages
sudo apt upgrade -y
# This may take 2 to 5 minutes

# Step 4: Check Python version (pre-installed in Kali)
python3 --version
# Expected output: Python 3.11.x

# Step 5: Install pip if not present
sudo apt install python3-pip -y

# Step 6: Install Git
sudo apt install git -y

# Step 7: Verify Git installation
git --version
# Expected output: git version 2.39.x
```

---

## Installation

### Step 1: Clone the Repository

```bash
# On Windows 11 VM, open PowerShell
# On Kali Linux, open Terminal

git clone https://github.com/rithika-ujjalsingh/IT-Support-Ticketing-System.git
# Expected: Cloning into IT-Support-Ticketing-System...
```

### Step 2: Navigate into the Project Folder

```bash
cd IT-Support-Ticketing-System
# You should now be inside the project folder
# Verify with:
ls
# Should show: ticketing_system.py, requirements.txt, README.md, etc.
```

### Step 3: Install Python Dependencies

```bash
# Windows
pip install -r requirements.txt

# Kali Linux
pip3 install -r requirements.txt

# Expected output lines:
# Collecting colorama
# Collecting tabulate
# Successfully installed colorama-0.4.6 tabulate-0.9.0
```

### Step 4: Initialize the Database

```bash
# Windows
python ticketing_system.py --init

# Kali Linux
python3 ticketing_system.py --init

# Expected output:
# Database initialized successfully!
# Created: tickets_db.json
# Created: logs/audit.log
```

### Step 5: Run the Application

```bash
# Windows
python ticketing_system.py

# Kali Linux
python3 ticketing_system.py

# Expected output:
# ==========================================
#   RIVI IT Support Ticketing System v1.0
# ==========================================
# [1] Create New Ticket
# [2] View All Tickets
# [3] Update Ticket
# [4] Escalate Ticket
# [5] Close Ticket
# [6] Dashboard
# [7] Export Report
# [0] Exit
```

---

## Usage Guide

### Creating Your First Ticket

```
Step 1: From main menu, press 1 and Enter
Step 2: Enter ticket title: User cannot login to email
Step 3: Select category:
        [1] Hardware
        [2] Software
        [3] Network
        [4] Account
        [5] Security
        Enter: 4
Step 4: Select priority:
        [1] P1 Critical
        [2] P2 High
        [3] P3 Medium
        [4] P4 Low
        Enter: 2
Step 5: Enter affected user email: john.doe@company.com
Step 6: Enter description: User reports Outlook login failing since 9AM today
Step 7: Press Enter to confirm

Expected output:
Ticket created successfully!
Ticket ID: TKT-0001
Status: Open
Priority: P2 High
SLA Response: 4 hours remaining
```

### Viewing All Tickets

```
Step 1: From main menu, press 2 and Enter
Step 2: Select filter:
        [A] Show all tickets
        [B] Filter by status
        [C] Filter by priority
        [D] Filter by category
        [E] Search by keyword
Step 3: Press A to see all tickets
Step 4: Tickets display in a table format with ID, Title, Priority, Status, SLA
```

### Escalating a Ticket

```
Step 1: From main menu, press 4 and Enter
Step 2: Enter Ticket ID: TKT-0001
Step 3: Select escalation target:
        [1] Escalate to L2 (Network/Server/AD issues)
        [2] Escalate to L3 (Security/Complex issues)
        [3] Escalate to Vendor
Step 4: Enter escalation notes:
        Password reset attempted twice. Issue persists.
        Possible Active Directory sync problem.
Step 5: Press Enter to confirm
Expected: Ticket TKT-0001 escalated to L2. Notification sent.
```

---

## Lab Exercises

### Exercise 1: Basic Ticket Workflow (30 minutes)

```
Scenario: Monday morning helpdesk simulation
Goal: Process 5 tickets from creation to closure

Task 1: Create P3 ticket
  Title: Printer not working in Room 204
  Category: Hardware
  User: mary.smith@company.com

Task 2: Create P2 ticket
  Title: VPN connection dropping every 30 minutes
  Category: Network
  User: james.wilson@company.com

Task 3: Create P4 ticket
  Title: Mouse scroll wheel not working
  Category: Hardware
  User: sarah.jones@company.com

Task 4: Create P1 ticket
  Title: File server DOWN all users affected
  Category: Network
  User: admin@company.com

Task 5: Create P2 ticket
  Title: Cannot access shared drive after password change
  Category: Account
  User: mike.taylor@company.com

Actions to perform:
- Close the P4 mouse ticket immediately (resolution: replace mouse)
- Escalate P1 server ticket to L2 immediately
- Set P2 VPN ticket status to In Progress
- Export daily report to CSV file
```

### Exercise 2: SLA Monitoring (20 minutes)

```
Priority SLA Reference Table:
  P1 Critical: 1 hour to respond, 4 hours to resolve
  P2 High:     4 hours to respond, 8 hours to resolve
  P3 Medium:   8 hours to respond, 24 hours to resolve
  P4 Low:      24 hours to respond, 72 hours to resolve

Task 1: Create one ticket of each priority level
Task 2: Open Dashboard and verify SLA timers are counting down
Task 3: View the SLA status column for each ticket
Task 4: Manually test SLA breach notification for P1
Task 5: Generate SLA compliance report and export to CSV
```

### Exercise 3: Escalation Decision Tree (20 minutes)

```
Instructions: For each scenario below, decide if it is L1, L2, or L3.
Create the ticket in the system with the correct escalation.

Scenario A: My laptop screen is black after Windows update
  Correct Answer: L1 — basic troubleshooting, check display, safe mode

Scenario B: Cannot RDP into the server from any workstation
  Correct Answer: L2 — server/network configuration issue

Scenario C: Received phishing email, may have clicked a malicious link
  Correct Answer: L3 — potential security incident, immediate escalation

Scenario D: Microsoft Excel keeps crashing when opening large files
  Correct Answer: L1 — Office repair or reinstall

Scenario E: New employee needs Active Directory account creation
  Correct Answer: L2 — AD admin access required

Scenario F: Internet is extremely slow for entire office
  Correct Answer: L2 — network/ISP/firewall investigation needed

Scenario G: User forgot Windows login password
  Correct Answer: L1 — password reset via AD or local admin
```

---

## Ticket Workflow

```
USER REPORTS ISSUE
       |
       v
L1 CREATES TICKET
       |
       v
L1 DIAGNOSES ISSUE
       |
   Can L1 solve it?
   /           \
 YES            NO
  |              |
  v              v
L1 RESOLVES   ESCALATE TO L2
  |              |
  v         Can L2 solve it?
CLOSE           /       \
TICKET        YES        NO
               |          |
               v          v
          L2 RESOLVES  ESCALATE TO L3
               |             |
               v             v
          CLOSE TICKET  L3 OR VENDOR RESOLVES
                             |
                             v
                        CLOSE TICKET
```

---

## Escalation Rules

| Situation | Action Required |
|-----------|----------------|
| Any P1 Critical ticket | Immediately escalate to L2 and notify manager |
| P2 ticket unresolved after 2 hours | Escalate to L2 |
| Issue involves Active Directory | Escalate to L2 |
| Issue involves servers or network devices | Escalate to L2 |
| Security incident suspected | Escalate to L3 immediately |
| Hardware failure on server or network | Escalate to L2 or L3 |
| Vendor software license issue | Escalate to Vendor via L3 |
| L1 has attempted fix twice and failed | Escalate to L2 |

---

## Project Structure

```
IT-Support-Ticketing-System/
|
├── ticketing_system.py       Main entry point and menu
├── ticket_manager.py         Ticket CRUD operations
├── database.py               JSON database handler
├── escalation.py             Escalation logic engine
├── sla_monitor.py            SLA timer and breach detection
├── reports.py                CSV export and dashboard
├── utils.py                  Color formatting and helper functions
├── requirements.txt          Python dependencies list
├── README.md                 This documentation file
├── SECURITY.md               Security policy
├── CONTRIBUTING.md           Contribution guidelines
├── tickets_db.json           Local ticket database auto-created on init
└── logs/
    └── audit.log             Complete audit trail of all actions
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithikaujjalsingh](https://www.linkedin.com/in/rithikaujjalsingh)

*Built for IT Support learners | RITHIKA UJJALSINGH 2026*
