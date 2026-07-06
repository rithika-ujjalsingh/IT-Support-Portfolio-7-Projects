# 🗂️ Active Directory User & Group Lifecycle Management

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L2-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project covers full Active Directory user lifecycle management on a Windows Server 2019 domain controller — from organizational unit design through user creation, group membership, domain join, account lockout handling, and password resets — using both the GUI (ADUC) and PowerShell, the way it's actually done in enterprise environments.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 | Domain Controller (`company.local`) | `192.168.100.10` |
| Windows 11 Pro | Domain-Joined Client | `192.168.100.20` |

**Hypervisor:** VMware Workstation Pro

## 🎯 Objectives

- Design an OU structure that mirrors a real company's department layout
- Create AD user accounts via both GUI and PowerShell
- Create a security group and manage group membership
- Join a Windows 11 client to the domain and verify login
- Simulate and resolve an account lockout
- Perform an administrative password reset with forced change at next logon
- Offboard a user (disable account + move to a "Disabled Users" OU)

## 🔧 Tools & Commands Used

`Active Directory Users and Computers (ADUC)` `PowerShell` `Active Directory module (New-ADUser, Get-ADUser, Unlock-ADAccount, Set-ADAccountPassword)`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Organizational Unit Structure

Created department-based OUs to mirror a real company hierarchy, rather than dumping all users into the default Users container.

```
ADUC → company.local → Right-click → New → Organizational Unit
Created: HR, Finance, IT, Disabled Users
```

📸 *Screenshot: `01-ou-structure-created.png`*

---

### Step 2 — New User Creation (GUI)

```
HR OU → Right-click → New → User
First Name: Nova   Last Name: Singh
Logon name: nova.singh
Password: Welcome@2024!  (User must change password at next logon: checked)
```

📸 *Screenshot: `02-new-user-aduc-wizard.png`*

---

### Step 3 — Security Group & Membership

Created a security group for the HR department and added the new user as a member, the standard model for permission/resource assignment.

```
HR OU → Right-click → New → Group
Name: HR-Team   Scope: Global   Type: Security
→ Add Members → nova.singh
```

📸 *Screenshot: `03-security-group-membership.png`*

---

### Step 4 — Domain Join (Windows 11 Client)

```
Win11 → Settings → Accounts → Access work or school → Connect
→ Join this device to a local Active Directory domain
→ Domain: company.local → Admin credentials → Restart
```

📸 *Screenshot: `04-domain-join-confirmation.png`*

---

### Step 5 — Login Verification

Logged in as the new domain user on the joined client to confirm the account and domain trust both worked end-to-end, not just in theory.

```
Other User → nova.singh → Welcome@2024! → forced password change → new profile created
```

📸 *Screenshot: `05-domain-user-first-login.png`*

---

### Step 6 — Account Lockout & Recovery (PowerShell)

Simulated a locked-out account (5 failed password attempts) and resolved it using PowerShell — the most common L2 helpdesk ticket in any AD environment.

```powershell
# Identify locked accounts
Search-ADAccount -LockedOut | Select Name, SamAccountName

# Unlock
Unlock-ADAccount -Identity "nova.singh"
```

📸 *Screenshot: `06-account-unlock-powershell.png`*

---

### Step 7 — Administrative Password Reset

```powershell
Set-ADAccountPassword -Identity "nova.singh" -Reset `
  -NewPassword (ConvertTo-SecureString "NewPass@2024!" -AsPlainText -Force)
Set-ADUser -Identity "nova.singh" -ChangePasswordAtLogon $true
```

📸 *Screenshot: `07-password-reset-confirmation.png`*

---

### Step 8 — Offboarding (Disable & Move)

```powershell
Disable-ADAccount -Identity "nova.singh"
Get-ADUser "nova.singh" | Move-ADObject -TargetPath "OU=Disabled Users,DC=company,DC=local"
```

📸 *Screenshot: `08-account-disabled-offboarded.png`*

---

## ✅ Resolution Summary

| Task | Method | Outcome |
|---|---|---|
| Department structure needed | Created 4 OUs | Clean, scalable hierarchy for GPO/permission targeting |
| New employee onboarding | ADUC GUI user creation | Account created with forced first-login password change |
| User locked out after failed logins | `Search-ADAccount -LockedOut` + `Unlock-ADAccount` | Account unlocked in under 1 minute |
| Forgotten password | `Set-ADAccountPassword -Reset` | New password issued with forced change at next logon |
| Employee resignation | `Disable-ADAccount` + `Move-ADObject` | Account safely disabled and archived, not deleted |

## 📚 What This Demonstrates

- End-to-end AD lifecycle management — not just account creation in isolation
- Comfort switching between GUI and PowerShell depending on what's faster for the task
- Understanding of the *why* behind offboarding practices (disable + archive, never delete immediately)
- Real troubleshooting of the #1 most common L2 ticket type: account lockouts

## 🗂️ Folder Structure

```
04-active-directory-lab/
├── README.md
└── screenshots/
    ├── 01-ou-structure-created.png
    ├── 02-new-user-aduc-wizard.png
    ├── 03-security-group-membership.png
    ├── 04-domain-join-confirmation.png
    ├── 05-domain-user-first-login.png
    ├── 06-account-unlock-powershell.png
    ├── 07-password-reset-confirmation.png
    └── 08-account-disabled-offboarded.png
```

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
