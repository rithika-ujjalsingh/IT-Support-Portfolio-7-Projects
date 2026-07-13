# Full Windows Server 2019 Lab Setup Automation
# Author: Rithika U | RIVI Enterprises
# Run on Windows Server 2019 AFTER promoting to Domain Controller

Import-Module ActiveDirectory -ErrorAction Stop

$Domain   = "rivi.local"
$DomainDN = "DC=rivi,DC=local"
$Password = ConvertTo-SecureString "Rivi@User2025!" -AsPlainText -Force

Write-Host "RIVI Lab Setup Starting..." -ForegroundColor Cyan

# Create OUs
$OUs = @("RIVI-Org","IT-Staff","End-Users","Computers","Security-Groups","Disabled-Accounts","Service-Accounts")
foreach ($OU in $OUs) {
    New-ADOrganizationalUnit -Name $OU -Path $DomainDN -ProtectedFromAccidentalDeletion $false -ErrorAction SilentlyContinue
    Write-Host "  OU: $OU" -ForegroundColor Green
}

# Create Groups
$GroupBase = "OU=Security-Groups,OU=RIVI-Org,$DomainDN"
$Groups = @("IT-Support-Team","VPN-Users","File-Share-Readonly","File-Share-Readwrite","Remote-Desktop-Users")
foreach ($G in $Groups) {
    New-ADGroup -Name $G -GroupScope Global -GroupCategory Security -Path $GroupBase -ErrorAction SilentlyContinue
    Write-Host "  Group: $G" -ForegroundColor Green
}

# Create Users
$ITBase   = "OU=IT-Staff,OU=RIVI-Org,$DomainDN"
$UserBase = "OU=End-Users,OU=RIVI-Org,$DomainDN"

New-ADUser -Name "Rithika U" -GivenName "Rithika" -Surname "U" -SamAccountName "rithika.u" `
    -UserPrincipalName "rithika.u@$Domain" -Department "IT Support" -Title "Security Engineer" `
    -AccountPassword $Password -Enabled $true -Path $ITBase -ErrorAction SilentlyContinue

New-ADUser -Name "Test User" -GivenName "Test" -Surname "User" -SamAccountName "test.user" `
    -UserPrincipalName "test.user@$Domain" -Department "HR" -Title "HR Specialist" `
    -AccountPassword $Password -Enabled $true -Path $UserBase -ErrorAction SilentlyContinue

# Add to groups
Add-ADGroupMember -Identity "IT-Support-Team" -Members "rithika.u" -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity "VPN-Users" -Members "rithika.u" -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity "File-Share-Readonly" -Members "test.user" -ErrorAction SilentlyContinue

# DNS Records
Add-DnsServerResourceRecordA -ZoneName $Domain -Name "WIN11-CLIENT" -IPv4Address "192.168.100.102" -ErrorAction SilentlyContinue
Add-DnsServerResourceRecordA -ZoneName $Domain -Name "KALI-LINUX" -IPv4Address "192.168.100.20" -ErrorAction SilentlyContinue

Write-Host "`nLab setup complete! Domain: $Domain" -ForegroundColor Green
Write-Host "Users: rithika.u, test.user | Password: Rivi@User2025!" -ForegroundColor Yellow
