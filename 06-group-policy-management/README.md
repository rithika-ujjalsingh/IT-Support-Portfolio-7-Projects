# 🛡️ Group Policy Management & Enforcement Lab

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L2-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project covers authoring, linking, and verifying Group Policy Objects (GPOs) on a Windows Server 2019 domain controller — the primary mechanism enterprises use to enforce security baselines and manage client configuration centrally, rather than touching every machine by hand.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 (DC01) | Domain Controller / GPO Authoring | `192.168.100.10` |
| Windows 11 Pro | Domain-joined Client | `192.168.100.25` |

**Hypervisor:** VMware Workstation Pro
**Domain:** `corp.local`

## 🎯 Objectives

- Enforce a strong password policy via Group Policy
- Configure an automatic screen lock for idle sessions
- Confirm GPOs are correctly linked at the domain level
- Force and verify policy application on a client
- Restrict removable storage (USB) access for security compliance
- Deploy a mapped network drive via Group Policy Preferences

## 🔧 Tools & Commands Used

`Group Policy Management Console (gpmc.msc)` `gpupdate` `Group Policy Modeling Wizard` `File Sharing (Advanced Sharing)`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Password Policy GPO

gpmc.msc → New GPO: "Password Policy"

Computer Config → Security Settings → Account Policies → Password Policy

Minimum password length: 12 | Complexity requirements: Enabled

📸 *Screenshot: `01-password-policy-gpo-settings.png`*

---

### Step 2 — Screen Lock Policy GPO

New GPO: "Screen Lock Policy"

User Config → Admin Templates → Control Panel → Personalization

Enable screen saver: Enabled | Screen saver timeout: 600 sec

📸 *Screenshot: `02-screen-lock-policy-settings.png`*

---

### Step 3 — GPO Linkage Verification

Confirmed both new GPOs, along with the existing Account Lockout and Default Domain policies, were correctly linked and enabled at the domain level.

📸 *Screenshot: `03-gpo-linked-to-domain.png`*

---

### Step 4 — Force Policy Update

```cmd
gpupdate /force
```

📸 *Screenshot: `04-gpupdate-force-output.png`*

---

### Step 5 — Policy Application Verification

> **Troubleshooting note:** Attempted to verify with `gpresult /R` directly on the client, but the account in use was a local profile rather than the domain account, so no domain GPOs appeared as applied. Switching to a domain login hit a sign-in restriction, and a remote `gpresult` query from the DC failed due to WMI/RPC connectivity. Used the **Group Policy Modeling Wizard** on the DC instead to simulate policy application for the domain user and OU — this avoids the client-side dependency entirely and confirmed the Group Policy Infrastructure, Registry, and Security components all processed successfully.

📸 *Screenshot: `05-gpresult-applied-gpos.png`*

---

### Step 6 — Removable Storage Restriction

New GPO: "Block Removable Storage"
Computer Config → Admin Templates → System → Removable Storage Access
All Removable Storage classes: Deny all access → Enabled

📸 *Screenshot: `06-usb-block-policy-settings.png`*

---

### Step 7 — Drive Mapping via Group Policy Preferences

User Config → Preferences → Windows Settings → Drive Maps → New → Mapped Drive
Location: \192.168.100.10\HR-Share   Drive Letter: H:

📸 *Screenshot: `07-drive-mapping-gpo.png`*

---

### Step 8 — Mapped Drive Verification

> **Troubleshooting note:** Initial testing failed with "Windows cannot access \\192.168.100.10\HR-Share" — Windows Network Diagnostics confirmed the server was reachable but the share itself didn't exist yet. Created and shared the `HR-Share` folder on the DC, after which the path resolved successfully and was browsable from the client — a practical reminder that GPO drive mappings depend on the underlying file share being provisioned first.

📸 *Screenshot: `08-mapped-drive-visible-client.png`*

---

## ✅ Resolution Summary

| Task | Configuration | Outcome |
|---|---|---|
| Weak passwords across the domain | Password Policy GPO (12 char min + complexity) | Enforced domain-wide |
| Unattended sessions left unlocked | Screen Lock Policy GPO (10 min timeout) | Auto-lock enforced |
| Uncertain if policies were live | `gpupdate /force` + Group Policy Modeling | Confirmed successful application |
| Data exfiltration risk via USB | Removable Storage Access GPO | All removable storage denied |
| Manual drive mapping for every user | Drive Maps preference in GPO | H: drive auto-provisioned, diagnosed and fixed missing share |

## 📚 What This Demonstrates

- Ability to author GPOs from scratch for real security requirements, not just edit existing ones
- Systematic troubleshooting when a verification method fails — switching approaches (client gpresult → DC-side modeling) rather than getting stuck
- Understanding that GPO deployment often depends on other infrastructure (a share existing, WMI/RPC connectivity) being in place
- Comfort working across both Group Policy security settings and preference-based deployment (drive maps)

## 🗂️ Folder Structure

06-group-policy-management/
├── README.md
└── screenshots/
├── 01-password-policy-gpo-settings.png
├── 02-screen-lock-policy-settings.png
├── 03-gpo-linked-to-domain.png
├── 04-gpupdate-force-output.png
├── 05-gpresult-applied-gpos.png
├── 06-usb-block-policy-settings.png
├── 07-drive-mapping-gpo.png
└── 08-mapped-drive-visible-client.png

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
