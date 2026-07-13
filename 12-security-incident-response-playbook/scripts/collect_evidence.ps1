# Security Incident Evidence Collection Script
# Author: Rithika U | RIVI Enterprises

param([string]$IncidentId = "IR-$(Get-Date -Format 'yyyyMMdd-HHmm')")

$EvidenceDir = "C:\IR-Evidence\$IncidentId"
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

Write-Host "RIVI Evidence Collector | Incident: $IncidentId" -ForegroundColor Cyan

function Save { param([string]$Name, [scriptblock]$Cmd)
    Write-Host "  Collecting: $Name" -ForegroundColor Yellow
    try { & $Cmd | Out-File "$EvidenceDir\$Name.txt" -Encoding UTF8 }
    catch { "Error: $_" | Out-File "$EvidenceDir\$Name.txt" }
}

Save "01_system_info"         { systeminfo }
Save "02_processes"           { Get-Process | Sort-Object CPU -Descending | Select-Object Name, Id, CPU | Format-Table }
Save "03_network_connections" { netstat -ano }
Save "04_logged_on_users"     { query user }
Save "05_local_admins"        { Get-LocalGroupMember -Group "Administrators" }
Save "06_scheduled_tasks"     { Get-ScheduledTask | Where-Object State -ne "Disabled" | Select-Object TaskName, State }
Save "07_running_services"    { Get-Service | Where-Object Status -eq "Running" | Select-Object Name, DisplayName }
Save "08_dns_cache"           { ipconfig /displaydns }
Save "09_arp_table"           { arp -a }
Save "10_logins_24h"          { Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624;StartTime=(Get-Date).AddHours(-24)} -EA SilentlyContinue | Select-Object TimeCreated, Message | Format-List }
Save "11_failed_logins_24h"   { Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625;StartTime=(Get-Date).AddHours(-24)} -EA SilentlyContinue | Select-Object TimeCreated, Message | Format-List }
Save "12_lockouts"            { Get-WinEvent -FilterHashtable @{LogName='Security';Id=4740} -EA SilentlyContinue | Select-Object TimeCreated, Message | Format-List }
Save "13_new_accounts_7d"     { Get-WinEvent -FilterHashtable @{LogName='Security';Id=4720;StartTime=(Get-Date).AddDays(-7)} -EA SilentlyContinue | Select-Object TimeCreated, Message | Format-List }

Get-ChildItem $EvidenceDir -File | Get-FileHash -Algorithm SHA256 |
    Export-Csv "$EvidenceDir\00_EVIDENCE_HASHES.csv" -NoTypeInformation

Write-Host "Evidence saved to: $EvidenceDir" -ForegroundColor Green
Write-Host "SHA256 hashes logged in 00_EVIDENCE_HASHES.csv" -ForegroundColor Green
