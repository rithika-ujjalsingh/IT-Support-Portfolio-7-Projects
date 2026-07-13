# Active Directory User Management Scripts — L2 Practical Lab

![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-5391FE?style=for-the-badge&logo=powershell)
![Level](https://img.shields.io/badge/Level-L2%20IT%20Support-0096FF?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20Server%202019-0078D4?style=for-the-badge)

> Complete Active Directory user lifecycle management via PowerShell scripts. Covers user creation, group management, password resets, account lockouts, bulk operations, and audit reporting.

---

## Overview

Active Directory management is a core L2 skill. This project provides ready-to-use PowerShell scripts for every common AD task an L2 support engineer will face daily.

**VM Setup Used:**
- Windows Server 2019 (Domain Controller): `192.168.100.10`
- Windows 11 (Client, joined to domain): `192.168.100.102`
- Kali Linux (monitoring): `192.168.100.20`

**Domain used in all examples:** `rivi.local`

**What you will learn:**
- Active Directory PowerShell module commands
- User account lifecycle management
- Group membership management
- Password policy enforcement
- Account lockout investigation
- Bulk operations with CSV import
- Audit and compliance reporting

---

## Prerequisites

### On Windows Server 2019 (192.168.100.10)

```powershell
# Step 1: Open PowerShell as Administrator
# Click Start, type PowerShell, right-click, Run as Administrator

# Step 2: Verify AD DS role is installed
Get-WindowsFeature AD-Domain-Services
# Expected: Installed = True

# Step 3: Verify Active Directory module is available
Import-Module ActiveDirectory
Get-Module ActiveDirectory
# Expected: Shows the module loaded with version number

# Step 4: Check domain info
Get-ADDomain
# Expected: Shows domain name rivi.local, DomainMode, PDCEmulator, etc.

# Step 5: Check you can query users
Get-ADUser -Filter * | Select-Object Name, SamAccountName | Sort-Object Name
# Expected: List of existing users in the domain
```

### On Windows 11 Client (192.168.100.102)

```powershell
# Step 1: Verify machine is joined to domain
systeminfo | findstr "Domain"
# Expected: Domain: rivi.local

# Step 2: Install RSAT tools to manage AD from client
# Open Settings → Apps → Optional Features → Add Feature
# Search for: RSAT Active Directory
# Install: RSAT: Active Directory Domain Services and Lightweight Directory Tools

# Step 3: Alternatively, install via PowerShell
Add-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"

# Step 4: Test AD access from client
Import-Module ActiveDirectory
Get-ADUser -Filter * | Measure-Object
# Expected: Count shows number of users
```

---

## Installation

### Step 1: Clone the Repository on Windows Server

```powershell
# Open PowerShell on Windows Server 2019

# Step 1a: Navigate to a working directory
cd C:\IT-Support-Projects

# Step 1b: If C:\IT-Support-Projects does not exist, create it
New-Item -ItemType Directory -Path "C:\IT-Support-Projects" -Force

# Step 1c: Clone from GitHub
git clone https://github.com/rithika-ujjalsingh/AD-User-Management-Scripts.git

# Step 1d: Navigate into folder
cd AD-User-Management-Scripts

# Step 1e: List files to confirm
Get-ChildItem
# Expected: manage_users.ps1, bulk_create.ps1, audit_report.ps1, etc.
```

### Step 2: Set PowerShell Execution Policy

```powershell
# By default, Windows blocks unsigned scripts. Run this to allow:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Press Y when prompted

# Verify the policy
Get-ExecutionPolicy
# Expected: RemoteSigned
```

### Step 3: Test Basic Connection

```powershell
# Run the connection test
.\test_connection.ps1

# Expected output:
# [PASS] Connected to domain: rivi.local
# [PASS] Active Directory module loaded
# [PASS] Can query users: 15 users found
# [PASS] Can query groups: 8 groups found
# Ready to use AD management scripts!
```

---

## Usage Guide

### Script 1: Create a Single User

```powershell
# Syntax
.\manage_users.ps1 -Action Create -FirstName <name> -LastName <name> -Department <dept> -Title <title>

# Example: Create a new IT Support user
.\manage_users.ps1 -Action Create `
    -FirstName "Priya" `
    -LastName "Sharma" `
    -Department "IT Support" `
    -Title "L1 Support Engineer" `
    -Manager "john.doe"

# Expected output:
# Creating user: priya.sharma
# Setting password...
# Adding to groups: Domain Users, IT-Support-Team
# Enabling account...
# User created successfully!
# Username: priya.sharma
# Email: priya.sharma@rivi.local
# OU: OU=IT,DC=rivi,DC=local
# Temporary Password: Rivi@2025! (must change on first login)
```

### Script 2: Reset a Password

```powershell
# Syntax
.\manage_users.ps1 -Action ResetPassword -Username <samaccountname>

# Example
.\manage_users.ps1 -Action ResetPassword -Username priya.sharma

# Expected output:
# Locating user: priya.sharma
# User found: Priya Sharma (IT Support)
# Account Status: Enabled
# Last Password Change: 2025-06-01
# Resetting password...
# New temporary password: TempPass@123
# User must change password at next login: YES
# Password reset successful!
```

### Script 3: Unlock a Locked Account

```powershell
# First, CHECK if an account is locked before unlocking
.\manage_users.ps1 -Action CheckLock -Username priya.sharma

# Expected output:
# User: Priya Sharma
# Locked: YES
# Lockout Time: 2025-07-01 09:45:23
# Bad Password Count: 5
# Last Bad Password: 2025-07-01 09:45:23
# Lockout Source: DESKTOP-WIN11 (192.168.100.102)

# Now unlock the account
.\manage_users.ps1 -Action Unlock -Username priya.sharma

# Expected output:
# Unlocking account: priya.sharma
# Account unlocked successfully!
# Advise user: Check Caps Lock, verify correct password
```

### Script 4: Disable a User (Employee Leaving)

```powershell
# Disable user account properly (do not delete immediately)
.\manage_users.ps1 -Action Disable -Username priya.sharma -Reason "Employee resigned 2025-07-01"

# Expected output:
# Disabling account: priya.sharma
# Removing from all groups except Domain Users...
# Moving to OU=Disabled-Accounts,DC=rivi,DC=local
# Setting description: DISABLED on 2025-07-01 - Employee resigned
# Account disabled and moved to disabled OU.
# Note: Account will be auto-deleted after 30 days per policy.
```

### Script 5: Bulk Create Users from CSV

```powershell
# Step 1: Create the CSV file with user data
# Open Notepad and create users.csv with this content:
# FirstName,LastName,Department,Title,Manager
# Ananya,Kumar,HR,HR Specialist,hr.manager
# Karthik,Rajan,Finance,Accountant,finance.lead
# Deepa,Nair,IT Support,L1 Engineer,it.manager

# Step 2: Run bulk create
.\bulk_create.ps1 -CsvFile "users.csv"

# Expected output:
# Processing 3 users from users.csv
# [1/3] Creating: ananya.kumar - SUCCESS
# [2/3] Creating: karthik.rajan - SUCCESS
# [3/3] Creating: deepa.nair - SUCCESS
# Bulk creation complete!
# Success: 3
# Failed: 0
# Log saved: bulk_create_20250701.log
```

### Script 6: Generate Audit Report

```powershell
# Generate complete AD audit report
.\audit_report.ps1

# Expected output files:
# report_ad_users_20250701.csv    — All user accounts with status
# report_disabled_users.csv       — Accounts disabled > 30 days
# report_never_logged_in.csv      — Accounts created but never used
# report_password_expiry.csv      — Passwords expiring in next 14 days
# report_admin_accounts.csv       — All accounts with admin privileges
```

---

## Lab Exercises

### Exercise 1: New Employee Onboarding (30 minutes)

```
Scenario: New employee joining IT Support team tomorrow

Task 1: Create user account
  First Name: Rahul
  Last Name: Menon
  Department: IT Support
  Title: L1 Support Engineer
  Manager: your own username

Task 2: Verify account was created correctly
  Get-ADUser rahul.menon -Properties *
  Check: Enabled = True, Department = IT Support, PasswordMustChange = True

Task 3: Add to correct groups
  Add-ADGroupMember -Identity "IT-Support-Team" -Members rahul.menon
  Add-ADGroupMember -Identity "VPN-Users" -Members rahul.menon

Task 4: Verify group memberships
  Get-ADPrincipalGroupMembership rahul.menon | Select-Object Name

Task 5: Test login from Windows 11 VM
  On 192.168.100.102, sign out
  Login with: RIVI\rahul.menon and the temp password
  System should force password change
  Set new password: RahuL@IT2025
  Verify desktop loads and can access shared drives
```

### Exercise 2: Account Lockout Investigation (20 minutes)

```
Scenario: User calls saying cannot login, account locked

Task 1: Check account status
  .\manage_users.ps1 -Action CheckLock -Username rahul.menon

Task 2: Find lockout source
  Get-WinEvent -ComputerName WIN-SERVER-2019 -FilterHashtable @{
    LogName = 'Security'
    Id = 4740
  } | Select-Object TimeCreated, Message | Format-List

  Event ID 4740 = Account Lockout event
  Event ID 4625 = Failed login attempt

Task 3: Identify the machine causing lockout
  Look for "Caller Computer Name" in Event ID 4740
  This tells you which computer had wrong cached credentials

Task 4: Resolve the issue
  Option A: Unlock the account
    .\manage_users.ps1 -Action Unlock -Username rahul.menon
  
  Option B: Fix credentials on the source machine
    On the offending machine, open Credential Manager
    Remove any saved credentials for the domain
    Then unlock account

Task 5: Document what you found in a ticket
```

### Exercise 3: Employee Offboarding (20 minutes)

```
Scenario: Employee Rahul Menon resigned today

Task 1: Disable the account immediately
  .\manage_users.ps1 -Action Disable -Username rahul.menon -Reason "Resigned 2025-07-01"

Task 2: Remove from all security groups
  Get-ADPrincipalGroupMembership rahul.menon
  Remove from any special access groups (keep only Domain Users)

Task 3: Set out-of-office on mailbox
  (In real environment: use Exchange or M365 admin)
  For lab: update AD Description field
  Set-ADUser rahul.menon -Description "DISABLED - Resigned 2025-07-01 - Contact manager"

Task 4: Move to Disabled OU
  Move-ADObject "CN=Rahul Menon,OU=IT,DC=rivi,DC=local" `
    -TargetPath "OU=Disabled-Accounts,DC=rivi,DC=local"

Task 5: Generate audit report confirming all access removed
  .\audit_report.ps1
  Verify rahul.menon appears in disabled report
```

---

## Common AD Commands Reference

```powershell
# USER MANAGEMENT
Get-ADUser -Filter *                              # List all users
Get-ADUser -Identity "username" -Properties *    # Get all user properties
New-ADUser -Name "John Doe"                       # Create user
Set-ADUser -Identity "username" -Title "Manager" # Update user attribute
Remove-ADUser -Identity "username"                # Delete user (permanent)
Disable-ADAccount -Identity "username"            # Disable account
Enable-ADAccount -Identity "username"             # Enable account
Unlock-ADAccount -Identity "username"             # Unlock locked account
Set-ADAccountPassword -Identity "username"        # Reset password

# GROUP MANAGEMENT
Get-ADGroup -Filter *                             # List all groups
Get-ADGroupMember -Identity "GroupName"           # List group members
Add-ADGroupMember -Identity "GroupName" -Members "username"    # Add to group
Remove-ADGroupMember -Identity "GroupName" -Members "username" # Remove from group
Get-ADPrincipalGroupMembership "username"         # Show user's groups

# PASSWORD MANAGEMENT
Search-ADAccount -LockedOut                       # Find locked accounts
Search-ADAccount -PasswordExpired                 # Find expired passwords
Search-ADAccount -AccountDisabled                 # Find disabled accounts

# COMPUTER MANAGEMENT
Get-ADComputer -Filter *                          # List all computers
Get-ADComputer -Identity "DESKTOP-WIN11"          # Single computer info
```

---

## Project Structure

```
AD-User-Management-Scripts/
|
├── manage_users.ps1          Main user management script
├── bulk_create.ps1           Bulk user creation from CSV
├── audit_report.ps1          Comprehensive AD audit reporting
├── test_connection.ps1       Verify AD connectivity
├── templates/
│   └── users_template.csv    CSV template for bulk creation
├── logs/                     Auto-created log directory
├── reports/                  Auto-created reports directory
├── README.md                 This documentation file
├── SECURITY.md               Security policy
└── CONTRIBUTING.md           Contribution guidelines
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithika-u](https://linkedin.com/in/rithika-u)

*Built for IT Support learners | RIVI Enterprises 2025*
