# Security Incident Response Playbook — L3 Practical Lab

![Security](https://img.shields.io/badge/Security-Incident%20Response-FF0000?style=for-the-badge&logo=shield)
![Level](https://img.shields.io/badge/Level-L3%20IT%20Support-7B2FBE?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows%20Server-1a1a2e?style=for-the-badge)
![MITRE](https://img.shields.io/badge/MITRE%20ATT%26CK-Mapped-FF4500?style=for-the-badge)

> Complete Security Incident Response Playbook with hands-on simulation labs.
> Covers account compromise, ransomware response, phishing investigation, and insider threat detection.

## Ethical Use Disclaimer

This project is for EDUCATIONAL PURPOSES ONLY.
All simulations must be performed ONLY on systems you own or have explicit written permission to test.
Unauthorized access is illegal under IT Act 2000 (India) and CFAA (USA).

---

## Overview

VM Setup:
- Windows Server 2019 (victim server): 192.168.100.10
- Windows 11 Client (victim workstation): 192.168.100.102
- Kali Linux (analyst and simulator): 192.168.100.20
Domain: rivi.local

MITRE ATT&CK Techniques Covered:
- T1078 Valid Accounts (Account Compromise)
- T1566 Phishing
- T1486 Data Encrypted for Impact (Ransomware)
- T1098 Account Manipulation
- T1110 Brute Force

---

## Playbook 1: Account Compromise Response

### Scenario
A user reports they cannot log in. IT notices unusual login times.
Suspected: Attacker has gained access to user credentials.

### Phase 1: Detection and Triage (First 15 minutes)

Run on Windows Server 2019 as Administrator in PowerShell:

```powershell
# Step 1: Check for unusual successful logins in last 24 hours
# Event ID 4624 = Successful logon
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624; StartTime=(Get-Date).AddHours(-24)} |
  Select-Object TimeCreated, Message | Out-File C:\incident_logins.txt
Write-Host "Saved to C:\incident_logins.txt"

# Step 2: Check for failed logins (brute force evidence)
# Event ID 4625 = Failed logon
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-24)} |
  Select-Object TimeCreated, Message | Out-File C:\incident_failed_logins.txt

# Step 3: Check account lockout events
# Event ID 4740 = Account locked out
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4740} -ErrorAction SilentlyContinue |
  Select-Object -First 10 TimeCreated, Message | Format-List

# Step 4: List currently logged on users
query user

# Step 5: Check unusual processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name, Id, CPU
```

### Phase 2: Containment (Minutes 15 to 30)

```powershell
# Step 1: Disable compromised account immediately
Disable-ADAccount -Identity "john.doe"
Write-Host "Account john.doe DISABLED" -ForegroundColor Red

# Step 2: Force logoff any active sessions
# Get session ID from: query user
logoff 2 /server:WIN-SERVER-2019

# Step 3: Reset password immediately
$NewPwd = ConvertTo-SecureString "EmergencyReset@2025!" -AsPlainText -Force
Set-ADAccountPassword -Identity "john.doe" -NewPassword $NewPwd -Reset

# Step 4: Check user group memberships for unauthorized additions
Get-ADPrincipalGroupMembership "john.doe" | Select-Object Name

# Step 5: Check local admin accounts for new unauthorized additions
Get-LocalGroupMember -Group "Administrators"

# Step 6: Block suspicious IP in Windows Firewall
netsh advfirewall firewall add rule name="BLOCK-ATTACKER-IP" dir=in action=block remoteip=203.0.113.50
```

### Phase 3: Recovery

```powershell
# Re-enable account after investigation complete
Enable-ADAccount -Identity "john.doe"
Set-ADAccountPassword -Identity "john.doe" `
  -NewPassword (ConvertTo-SecureString "NewSafe@2025!" -AsPlainText -Force) -Reset
Set-ADUser -Identity "john.doe" -ChangePasswordAtLogon $true
Write-Host "Account recovered and password reset. User must set new password on login."
```

---

## Playbook 2: Phishing Investigation

### Scenario
User clicked a link in a suspicious IT email asking for password.
Possible credential theft. Investigate and contain.

### Investigation on Kali Linux (192.168.100.20)

```bash
# Step 1: Check email headers for spoofed sender
# Open the email in plain text and look for Received: from lines
# Find the originating IP address (last Received: from entry)

# Step 2: Analyze suspicious URL headers WITHOUT visiting it
curl -I "http://suspicious-link.example.com"
# -I flag = HEAD request only, no page content is loaded

# Step 3: Download page content safely for analysis (no JavaScript executes)
wget -q -O /tmp/phishing_check.html "http://suspicious-link.example.com"
grep -i "password\|login\|credential\|signin" /tmp/phishing_check.html
# If these words appear: this is a credential harvesting page

# Step 4: Check IP reputation manually
# Go to these sites on your Kali browser:
# https://www.virustotal.com
# https://www.abuseipdb.com
# Enter the suspicious IP or URL
```

### Containment on Windows Server

```powershell
# Block phishing domain in internal DNS (sinkhole)
Add-DnsServerPrimaryZone -Name "phishingsite.example.com" -ReplicationScope Forest
Add-DnsServerResourceRecordA -ZoneName "phishingsite.example.com" `
    -Name "@" -IPv4Address "0.0.0.0"
Write-Host "Phishing domain blocked in DNS"

# If user entered credentials, follow Account Compromise Playbook immediately
Disable-ADAccount -Identity "affected.user"
Write-Host "Affected account disabled pending investigation"
```

---

## Playbook 3: Ransomware Response

### Scenario
Files have strange extensions. Ransom note on desktop.
Multiple users cannot open their documents.

### CRITICAL Immediate Actions (First 5 minutes)

```
ACTION 1: DISCONNECT the affected machine from network IMMEDIATELY
  - Unplug the ethernet cable physically (fastest method)
  - OR: Right-click network icon, Disable adapter
  - DO THIS BEFORE ANYTHING ELSE
  - Every second connected = more files encrypted = ransomware spreading

ACTION 2: Do NOT power off the machine
  - Leave it on but disconnected
  - Memory may contain the encryption key
  - Powering off may also trigger self-deletion of ransomware

ACTION 3: Take photos with your phone RIGHT NOW
  - Ransom note visible on screen
  - File listing showing encrypted extensions
  - Any error messages
  - These are forensic evidence for investigation

ACTION 4: Notify immediately
  - IT Manager
  - Security team (L3)
  - Company Management (if large-scale)
  - Do NOT post on social media

ACTION 5: Document the time everything was noticed
  - When user first reported issue
  - What time you disconnected the machine
  - Timeline is critical for forensics
```

### Assess Extent of Damage

```powershell
# From an UNAFFECTED admin machine only

# Find encrypted files on network shares
Get-ChildItem "\\WIN11-CLIENT\C$" -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.Extension -in @(".locked",".encrypted",".rivi",".WNCRY") } |
  Select-Object FullName, LastWriteTime |
  Export-Csv "C:\incident\encrypted_files.csv" -NoTypeInformation

# Check if Volume Shadow Copies exist (potential recovery without backup)
vssadmin list shadows
# If shadows exist: ransomware may not have deleted them yet
# This is your best recovery option if no backup exists
```

### Recovery Options (in order of preference)

```
Option 1: Restore from backup (BEST - fastest and cleanest)
  - Restore last known good backup from before the attack
  - Verify files are clean before restoring
  - Wipe and reimage the affected machine

Option 2: Volume Shadow Copy restore
  - Right-click affected folder in Windows Explorer
  - Properties tab, click Previous Versions
  - Restore from before the attack timestamp

Option 3: Free decryptor tool
  - Identify ransomware family first (file extension + ransom note)
  - Visit: https://www.nomoreransom.org
  - Download free decryptor if available for this family
  - Many older ransomware families have free decryptors

Option 4: Full rebuild (last resort)
  - Wipe machine completely
  - Fresh OS install
  - Restore DATA only from clean backup
  - Never restore executables from backup
```

---

## Playbook 4: Insider Threat Detection

### Monitoring Commands on Windows Server

```powershell
# Step 1: Find users with unusually high file access counts
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4663; StartTime=(Get-Date).AddDays(-7)} |
  Group-Object {$_.Properties[1].Value} |
  Sort-Object Count -Descending |
  Select-Object -First 10 Name, Count

# Step 2: Detect USB storage device usage
Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=(Get-Date).AddDays(-30)} |
  Where-Object {$_.Message -like "*USB*" -or $_.Message -like "*storage*"}

# Step 3: Check large amounts of files copied or moved
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4663; StartTime=(Get-Date).AddDays(-1)} |
  Where-Object {$_.Message -like "*Write*"} | Select-Object -First 20 TimeCreated, Message

# Step 4: Detect new admin accounts created
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4728; StartTime=(Get-Date).AddDays(-30)} |
  Select-Object TimeCreated, Message | Format-List
# Event 4728 = User added to security-enabled global group (including Administrators)
```

---

## Lab Simulation Exercise

### Simulate Brute Force Attack from Kali Linux

DISCLAIMER: Run this ONLY against your own lab VMs. Never against any real system.

```bash
# On Kali Linux (192.168.100.20)

# Step 1: Install Hydra brute force tool
sudo apt install hydra -y

# Step 2: Create test password wordlist
cat > /tmp/test_passwords.txt << WORDLIST
password
Password1
Admin@123
Rivi@2025
WrongPass1
WrongPass2
WrongPass3
WrongPass4
WrongPass5
WORDLIST

# Step 3: Run brute force against RDP on Windows 11
# This will trigger account lockout after 5 failed attempts
hydra -l test.user -P /tmp/test_passwords.txt rdp://192.168.100.102
```

### Detect the Attack on Windows Server

```powershell
# After running the simulation, detect it as an analyst

# Step 1: Find account lockout event
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4740} |
  Select-Object -First 3 TimeCreated, Message | Format-List

# Step 2: Find the source IP of the attacker
# Look for Source Network Address in the lockout event details
# Should show 192.168.100.20 (your Kali Linux)

# Step 3: Count failed attempts from that IP
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-1)} |
  Select-Object TimeCreated, Message | Format-List

# Step 4: Block the attacker IP
netsh advfirewall firewall add rule name="Block-Brute-Force-Kali" `
  dir=in action=block remoteip=192.168.100.20

# Step 5: Unlock the test user account
Unlock-ADAccount -Identity "test.user"
Write-Host "Attack detected, blocked, and account recovered!"
```

---

## Incident Report Template

Fill this out after every incident:

```
SECURITY INCIDENT REPORT

Incident ID:    IR-2025-XXX
Date Reported:  YYYY-MM-DD HH:MM
Date Occurred:  YYYY-MM-DD HH:MM
Reported By:    [Your name]
Severity:       Critical / High / Medium / Low

EXECUTIVE SUMMARY:
[Plain English summary of what happened, who was affected, and current status]

TIMELINE:
T+0 min:  [First detection or report]
T+X min:  [Containment action]
T+Y min:  [Resolution]

AFFECTED SYSTEMS:
- [Machine name and IP]

ATTACK VECTOR:
[How the attacker got in]

INDICATORS OF COMPROMISE (IOCs):
- IP Addresses: [suspicious IPs]
- File names: [malicious files]
- Event IDs triggered: [Windows Event IDs seen]
- Accounts compromised: [which user accounts]

CONTAINMENT ACTIONS:
1. [Step 1 taken and timestamp]
2. [Step 2 taken and timestamp]

ROOT CAUSE:
[Why did this happen? What security control failed?]

RECOVERY:
[How was the system restored to normal]

RECOMMENDATIONS:
1. [Specific action to prevent recurrence]
2. [Additional hardening measures]

Prepared by: Rithika U | RIVI Enterprises
```

---

## MITRE ATT&CK Mapping

| Technique | ID | Playbook |
|-----------|-----|---------|
| Valid Accounts | T1078 | Account Compromise |
| Phishing | T1566 | Phishing Investigation |
| Data Encrypted for Impact | T1486 | Ransomware Response |
| Account Manipulation | T1098 | Insider Threat |
| Brute Force | T1110 | Account Compromise |
| Remote Desktop Protocol | T1021.001 | Account Compromise |

---

## Project Structure

```
Security-Incident-Response-Playbook/
|
├── README.md                     This complete playbook
├── scripts/
│   ├── collect_evidence.ps1      Evidence collection automation
│   ├── containment.ps1           Quick containment script
│   └── brute_force_detector.ps1  Detect ongoing brute force
├── templates/
│   └── incident_report.md        Report template
├── SECURITY.md                   Security policy
└── CONTRIBUTING.md               Contribution guidelines
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithika-u](https://linkedin.com/in/rithika-u)

IT Act 2000 and CFAA compliance notice: Use only in authorized environments.

*Built for IT Support learners | RIVI Enterprises 2025*
