# Windows Server 2019 Lab Setup Guide — L2 Practical Lab

![Windows Server](https://img.shields.io/badge/Windows%20Server-2019-0078D4?style=for-the-badge&logo=windows)
![Level](https://img.shields.io/badge/Level-L2%20IT%20Support-0096FF?style=for-the-badge)
![Platform](https://img.shields.io/badge/VMware-Workstation-607078?style=for-the-badge)

> Complete step-by-step guide to set up Windows Server 2019 as a Domain Controller with DNS, DHCP, Active Directory, and Group Policy — from scratch in VMware.

---

## Overview

This project is a complete lab setup guide. Follow it to build a fully working enterprise-like IT environment using VMware with three VMs.

**Final Lab Environment:**
- Windows Server 2019: `192.168.100.10` — Domain Controller, DNS, DHCP, AD DS, File Server
- Windows 11 Client: `192.168.100.102` — Domain joined workstation
- Kali Linux: `192.168.100.20` — Monitoring and attack simulation

**Domain:** `rivi.local`

---

## Phase 1: Install Windows Server 2019 in VMware

### Step 1: Create the VM in VMware Workstation

```
1. Open VMware Workstation
2. Click "Create a New Virtual Machine"
3. Select "Typical (recommended)"
4. Select "Installer disc image file (ISO)"
5. Browse to your Windows Server 2019 ISO file
6. Click Next
7. Enter details:
   Full Name: Windows Server 2019
   (Skip product key for now)
8. Click Next
9. VM Name: WIN-SERVER-2019
   Location: D:\VMs\WIN-SERVER-2019 (or your preferred location)
10. Click Next
11. Disk size: 80 GB (minimum for lab use)
    Select "Store virtual disk as a single file"
12. Click Next
13. Click "Customize Hardware"
14. Set Memory: 4096 MB (4GB minimum)
15. Set Processors: 2
16. Network Adapter: Set to VMnet8 (NAT) or Host-only depending on your setup
17. Click Finish
```

### Step 2: Install Windows Server 2019

```
1. Power on the VM
2. Press any key to boot from DVD when prompted
3. Select Language: English
   Time format: depends on your region
   Keyboard: your keyboard layout
4. Click Next
5. Click "Install now"
6. Select edition: Windows Server 2019 Standard (Desktop Experience)
   NOTE: Must select Desktop Experience or you will get only command line
7. Accept license terms, click Next
8. Select: Custom: Install Windows only (advanced)
9. Select Drive 0 Unallocated Space
10. Click Next
11. Wait for installation (10 to 20 minutes)
12. Server will restart automatically
13. Set Administrator password when prompted
    Use a strong password: Rivi@Server2019!
    Confirm the password
14. Press Ctrl+Alt+Delete to login
    Username: Administrator
    Password: Rivi@Server2019!
15. Server Manager opens automatically — you are in!
```

### Step 3: Configure Static IP Address

```
All steps on Windows Server 2019:

1. Right-click the network icon in taskbar (bottom right)
2. Click "Open Network and Internet Settings"
3. Click "Change adapter options"
4. Right-click "Ethernet0" (or your adapter name)
5. Click "Properties"
6. Double-click "Internet Protocol Version 4 (TCP/IPv4)"
7. Select "Use the following IP address"
8. Enter:
   IP address: 192.168.100.10
   Subnet mask: 255.255.255.0
   Default gateway: 192.168.100.1
9. Select "Use the following DNS server addresses"
10. Preferred DNS: 127.0.0.1
    (The server will be its own DNS after AD setup)
11. Click OK
12. Click Close

Verify in PowerShell:
ipconfig /all
Should show IP 192.168.100.10 and DNS 127.0.0.1
```

### Step 4: Set Computer Name

```
1. Open Server Manager (it auto-opens on login)
2. Click "Local Server" in left sidebar
3. Click on the Computer Name (shows WIN-XXXXX by default)
4. System Properties window opens
5. Click "Change" next to "To rename this computer..."
6. Computer name: WIN-SERVER-2019
7. Click OK
8. Click OK again
9. Click "Restart Now" when prompted
10. Wait for restart (2 to 3 minutes)
11. Login again after restart
```

---

## Phase 2: Install Active Directory Domain Services

### Step 5: Add AD DS Role

```
1. Open Server Manager
2. Click "Add roles and features" (in the middle of the dashboard)
3. Click Next on Before You Begin
4. Select "Role-based or feature-based installation", click Next
5. Select your server (WIN-SERVER-2019), click Next
6. In Server Roles, check "Active Directory Domain Services"
7. A popup appears — click "Add Features"
8. Click Next
9. Click Next on Features (no changes needed)
10. Click Next on AD DS info page
11. Click "Install"
12. Wait for installation (3 to 5 minutes)
13. Click "Close" when done (do NOT restart yet)
```

### Step 6: Promote Server to Domain Controller

```
1. In Server Manager, you will see a warning flag at the top right
2. Click the flag icon
3. Click "Promote this server to a domain controller"
4. Select "Add a new forest"
5. Root domain name: rivi.local
6. Click Next
7. Domain Controller Options:
   Forest functional level: Windows Server 2016
   Domain functional level: Windows Server 2016
   DNS Server: CHECKED
   Global Catalog: CHECKED
   Domain controller password (DSRM): Rivi@DSRM2019!
8. Click Next
9. DNS Options — ignore the warning about delegation, click Next
10. NetBIOS domain name: RIVI (auto-filled), click Next
11. Paths: leave defaults, click Next
12. Review your options, click Next
13. Prerequisites Check will run (takes 1 to 2 minutes)
    Some yellow warnings are normal
14. Click "Install"
15. Server will automatically restart when done
16. After restart, login: RIVI\Administrator with your password
```

### Step 7: Verify Active Directory is Working

```powershell
# Open PowerShell as Administrator after restart

# Step 1: Check domain info
Get-ADDomain
# Expected: Shows rivi.local, DomainMode, PDCEmulator

# Step 2: Check AD DS service is running
Get-Service ADWS, KDC, NETLOGON, NTDS | Select-Object Name, Status
# Expected: All should show Status = Running

# Step 3: Check DNS is working
Resolve-DnsName rivi.local
# Expected: Shows IP 192.168.100.10

# Step 4: Check default OUs exist
Get-ADOrganizationalUnit -Filter *
# Expected: Shows Computers, Users, Domain Controllers, etc.
```

---

## Phase 3: Configure DNS

### Step 8: Verify and Test DNS

```powershell
# Check DNS server is installed and running
Get-WindowsFeature DNS
# Expected: Install State = Installed

Get-Service DNS
# Expected: Status = Running

# Open DNS Manager
# Start menu → Windows Administrative Tools → DNS

# Check Forward Lookup Zones
# You should see: rivi.local zone exists
# Under rivi.local you should see:
#   _msdcs, _sites, _tcp, _udp (auto-created by AD)
#   WIN-SERVER-2019 record pointing to 192.168.100.10

# Check Reverse Lookup Zone
# If not created, create it:
# Right-click Reverse Lookup Zones → New Zone
# Primary Zone → next
# IPv4 Reverse Lookup Zone → next
# Network ID: 192.168.100
# Click next, next, finish
```

### Step 9: Create DNS Records for Client VMs

```powershell
# Add DNS A record for Windows 11 client
Add-DnsServerResourceRecordA -ZoneName "rivi.local" `
    -Name "WIN11-CLIENT" `
    -IPv4Address "192.168.100.102"

# Add DNS A record for Kali Linux
Add-DnsServerResourceRecordA -ZoneName "rivi.local" `
    -Name "KALI-LINUX" `
    -IPv4Address "192.168.100.20"

# Verify both records exist
Get-DnsServerResourceRecord -ZoneName "rivi.local" -RRType A | Select-Object HostName, RecordData

# Test resolution
Resolve-DnsName WIN11-CLIENT.rivi.local
# Expected: Returns 192.168.100.102

Resolve-DnsName KALI-LINUX.rivi.local
# Expected: Returns 192.168.100.20
```

---

## Phase 4: Configure DHCP

### Step 10: Install DHCP Server Role

```
1. Open Server Manager
2. Click "Add roles and features"
3. Click Next, Next
4. In Server Roles, check "DHCP Server"
5. Click "Add Features" in popup
6. Click Next, Next, Next, Install
7. Wait for installation
8. Click "Complete DHCP configuration" link in notification
9. In the wizard:
   - Use RIVI\Administrator credentials
   - Click Commit
   - Click Close
```

### Step 11: Create DHCP Scope

```powershell
# Open PowerShell as Administrator

# Step 1: Create a new DHCP scope for lab network
Add-DhcpServerv4Scope `
    -Name "Lab Network Scope" `
    -StartRange 192.168.100.50 `
    -EndRange 192.168.100.200 `
    -SubnetMask 255.255.255.0 `
    -Description "IP addresses for lab clients"

# Step 2: Set default gateway for clients
Set-DhcpServerv4OptionValue `
    -ScopeId 192.168.100.0 `
    -Router 192.168.100.1

# Step 3: Set DNS server for clients
Set-DhcpServerv4OptionValue `
    -ScopeId 192.168.100.0 `
    -DnsServer 192.168.100.10

# Step 4: Set DNS domain name
Set-DhcpServerv4OptionValue `
    -ScopeId 192.168.100.0 `
    -DnsDomain "rivi.local"

# Step 5: Activate the scope
Set-DhcpServerv4Scope -ScopeId 192.168.100.0 -State Active

# Step 6: Verify scope is active
Get-DhcpServerv4Scope
# Expected: Shows scope 192.168.100.0 with State = Active

# Step 7: Create DHCP reservation for Windows 11 (optional but good practice)
Add-DhcpServerv4Reservation `
    -ScopeId 192.168.100.0 `
    -IPAddress 192.168.100.102 `
    -ClientId "00-11-22-33-44-55" `
    -Description "Windows 11 Client VM - Reserved"
    # Replace 00-11-22-33-44-55 with actual MAC from ipconfig /all on Win11
```

---

## Phase 5: Create Organizational Units and Users

### Step 12: Create Organizational Unit Structure

```powershell
# Create OU structure for the lab
$Domain = "DC=rivi,DC=local"

# Create top-level OUs
New-ADOrganizationalUnit -Name "RIVI-Org" -Path $Domain
New-ADOrganizationalUnit -Name "IT-Staff" -Path "OU=RIVI-Org,$Domain"
New-ADOrganizationalUnit -Name "End-Users" -Path "OU=RIVI-Org,$Domain"
New-ADOrganizationalUnit -Name "Computers" -Path "OU=RIVI-Org,$Domain"
New-ADOrganizationalUnit -Name "Security-Groups" -Path "OU=RIVI-Org,$Domain"
New-ADOrganizationalUnit -Name "Disabled-Accounts" -Path "OU=RIVI-Org,$Domain"
New-ADOrganizationalUnit -Name "Service-Accounts" -Path "OU=RIVI-Org,$Domain"

# Verify OUs were created
Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
```

### Step 13: Create Security Groups

```powershell
$BaseOU = "OU=Security-Groups,OU=RIVI-Org,DC=rivi,DC=local"

New-ADGroup -Name "IT-Support-Team" -GroupScope Global `
    -GroupCategory Security -Path $BaseOU `
    -Description "All IT Support staff"

New-ADGroup -Name "VPN-Users" -GroupScope Global `
    -GroupCategory Security -Path $BaseOU `
    -Description "Users allowed VPN access"

New-ADGroup -Name "File-Share-Readonly" -GroupScope Global `
    -GroupCategory Security -Path $BaseOU `
    -Description "Read-only access to shared files"

New-ADGroup -Name "File-Share-Readwrite" -GroupScope Global `
    -GroupCategory Security -Path $BaseOU `
    -Description "Read-write access to shared files"

# Verify groups
Get-ADGroup -Filter * | Select-Object Name, GroupScope, GroupCategory
```

### Step 14: Create Lab Users

```powershell
$IT_OU = "OU=IT-Staff,OU=RIVI-Org,DC=rivi,DC=local"
$User_OU = "OU=End-Users,OU=RIVI-Org,DC=rivi,DC=local"
$Password = ConvertTo-SecureString "Rivi@User2025!" -AsPlainText -Force

# Create IT Support user (for testing L1/L2 tasks)
New-ADUser -Name "Rithika U" -GivenName "Rithika" -Surname "U" `
    -SamAccountName "rithika.u" -UserPrincipalName "rithika.u@rivi.local" `
    -Department "IT Support" -Title "Security Engineer" `
    -AccountPassword $Password -Enabled $true -Path $IT_OU `
    -ChangePasswordAtLogon $false

# Create a standard end user
New-ADUser -Name "Test User" -GivenName "Test" -Surname "User" `
    -SamAccountName "test.user" -UserPrincipalName "test.user@rivi.local" `
    -Department "HR" -Title "HR Specialist" `
    -AccountPassword $Password -Enabled $true -Path $User_OU `
    -ChangePasswordAtLogon $false

# Add users to groups
Add-ADGroupMember -Identity "IT-Support-Team" -Members "rithika.u"
Add-ADGroupMember -Identity "VPN-Users" -Members "rithika.u"
Add-ADGroupMember -Identity "File-Share-Readwrite" -Members "rithika.u"
Add-ADGroupMember -Identity "File-Share-Readonly" -Members "test.user"

Write-Host "Users and groups configured successfully!" -ForegroundColor Green
```

---

## Phase 6: Join Windows 11 to Domain

### Step 15: Configure Windows 11 Network

```
On Windows 11 VM (192.168.100.102):

1. Right-click network icon in taskbar
2. Open Network and Internet Settings
3. Change adapter options
4. Right-click Ethernet → Properties
5. Double-click IPv4
6. Set static IP:
   IP: 192.168.100.102
   Subnet: 255.255.255.0
   Gateway: 192.168.100.1
   DNS: 192.168.100.10  ← This is the Windows Server DNS
7. Click OK

Verify connectivity:
Open CMD → ping 192.168.100.10
Should get replies from the server
```

### Step 16: Join Windows 11 to Domain

```
On Windows 11 VM:

1. Right-click Start → System
2. Click "Rename this PC (advanced)"
3. System Properties opens
4. Click "Change" button
5. Under "Member of", select "Domain"
6. Type: rivi.local
7. Click OK
8. Enter credentials when prompted:
   Username: RIVI\Administrator
   Password: Rivi@Server2019!
9. Click OK
10. You will see: Welcome to the rivi.local domain
11. Click OK
12. Click Close
13. Click "Restart Now"
14. After restart, on login screen:
    Click "Other user"
    Username: RIVI\rithika.u
    Password: Rivi@User2025!
    You are now logged in as a domain user!
```

---

## Phase 7: Configure Group Policy

### Step 17: Create and Apply Group Policies

```powershell
# On Windows Server, open PowerShell or Group Policy Management Console

# Create a new GPO for desktop settings
New-GPO -Name "IT-Desktop-Policy" -Comment "Standard desktop settings for IT staff"

# Link GPO to the IT-Staff OU
New-GPLink -Name "IT-Desktop-Policy" `
    -Target "OU=IT-Staff,OU=RIVI-Org,DC=rivi,DC=local"

# Create password policy GPO
New-GPO -Name "Password-Policy" -Comment "Domain password requirements"

# Open GPMC to configure policy settings:
# Start → Windows Administrative Tools → Group Policy Management
# Right-click "Password-Policy" → Edit
# Navigate to:
# Computer Configuration → Policies → Windows Settings → Security Settings → Account Policies
# Set:
#   Minimum password length: 8
#   Password complexity: Enabled
#   Maximum password age: 90 days
#   Account lockout threshold: 5 attempts
#   Account lockout duration: 30 minutes

# Force policy update on client after making changes
# Run on Windows 11 client:
# gpupdate /force

# Verify policy applied:
# gpresult /r
```

---

## Lab Exercises

### Exercise 1: Full Environment Verification (30 minutes)

```
Run these checks to verify your lab is set up correctly:

Check 1: From Windows 11, ping the server
  cmd → ping 192.168.100.10
  Expected: 4 replies with TTL

Check 2: From Windows 11, resolve domain
  cmd → nslookup rivi.local
  Expected: Shows IP 192.168.100.10

Check 3: Log in as domain user on Windows 11
  Logout current user
  Login with RIVI\test.user and password
  Expected: Desktop loads successfully

Check 4: From Kali Linux, ping the server
  Terminal → ping 192.168.100.10
  Expected: 4 packets, 0% loss

Check 5: Verify DHCP is working
  On Windows 11, set IP to DHCP (not static)
  Run: ipconfig /renew
  Expected: Gets IP in range 192.168.100.50 to 200

Check 6: Verify Active Directory Users and Computers
  On Server, open Active Directory Users and Computers
  Should see rivi.local domain with all your OUs and users
```

---

## Project Structure

```
Windows-Server-Lab-Setup/
|
├── README.md                    This complete guide
├── scripts/
│   ├── setup_ad.ps1             Full AD setup automation
│   ├── create_ous.ps1           OU and group creation
│   ├── create_users.ps1         Sample user creation
│   ├── configure_dhcp.ps1       DHCP scope setup
│   └── verify_lab.ps1           Verification checks
├── screenshots/                 Expected screenshots at each step
├── SECURITY.md                  Security policy
└── CONTRIBUTING.md              Contribution guidelines
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithika-u](https://linkedin.com/in/rithika-u)

*Built for IT Support learners | RIVI Enterprises 2025*
