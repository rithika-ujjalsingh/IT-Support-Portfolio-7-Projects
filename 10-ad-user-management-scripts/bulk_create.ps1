<#
.SYNOPSIS
    Bulk create Active Directory users from CSV file
.DESCRIPTION
    Author: Rithika U | RIVI Enterprises
.PARAMETER CsvFile
    Path to CSV file with columns: FirstName,LastName,Department,Title,Manager
.EXAMPLE
    .\bulk_create.ps1 -CsvFile "users.csv"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$CsvFile
)

Import-Module ActiveDirectory -ErrorAction Stop

$Domain = "rivi.local"
$DefaultOU = "OU=Users,DC=rivi,DC=local"
$LogFile = "logs\bulk_create_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

New-Item -ItemType Directory -Path "logs" -Force | Out-Null

function Log($Message) {
    $Line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Write-Host $Line
    Add-Content -Path $LogFile -Value $Line
}

if (-not (Test-Path $CsvFile)) {
    Write-Host "[FAIL] CSV file not found: $CsvFile" -ForegroundColor Red
    exit 1
}

$Users = Import-Csv $CsvFile
$Total = $Users.Count
$Success = 0
$Failed = 0

Log "Starting bulk user creation — $Total users from $CsvFile"

$i = 0
foreach ($User in $Users) {
    $i++
    $SamAccount = "$($User.FirstName.ToLower()).$($User.LastName.ToLower())"
    $DisplayName = "$($User.FirstName) $($User.LastName)"
    $Email = "$SamAccount@$Domain"
    $TempPassword = "Rivi@2025!"
    
    try {
        # Check if user already exists
        $Exists = Get-ADUser -Filter "SamAccountName -eq '$SamAccount'" -ErrorAction SilentlyContinue
        if ($Exists) {
            Log "[$i/$Total] SKIP: $SamAccount already exists"
            continue
        }
        
        New-ADUser `
            -Name $DisplayName `
            -GivenName $User.FirstName `
            -Surname $User.LastName `
            -SamAccountName $SamAccount `
            -UserPrincipalName $Email `
            -EmailAddress $Email `
            -Department $User.Department `
            -Title $User.Title `
            -Path $DefaultOU `
            -AccountPassword (ConvertTo-SecureString $TempPassword -AsPlainText -Force) `
            -ChangePasswordAtLogon $true `
            -Enabled $true
        
        $Success++
        Log "[$i/$Total] SUCCESS: Created $SamAccount ($DisplayName) - $($User.Department)"
    } catch {
        $Failed++
        Log "[$i/$Total] FAILED: $SamAccount - Error: $_"
    }
}

Log "Bulk creation complete! Success: $Success | Failed: $Failed | Total: $Total"
Log "Log file saved: $LogFile"
