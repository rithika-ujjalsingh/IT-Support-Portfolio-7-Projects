<#
.SYNOPSIS
    Active Directory User Management Script
.DESCRIPTION
    Complete AD user lifecycle management for L2 IT Support
    Author: Rithika U | RIVI Enterprises
.PARAMETER Action
    Action to perform: Create, ResetPassword, Unlock, CheckLock, Disable, Enable, Info
.PARAMETER Username
    SAM Account Name (login name) of the user
.EXAMPLE
    .\manage_users.ps1 -Action Create -FirstName "Priya" -LastName "Sharma" -Department "IT Support" -Title "L1 Engineer"
    .\manage_users.ps1 -Action Unlock -Username priya.sharma
    .\manage_users.ps1 -Action ResetPassword -Username priya.sharma
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Create","ResetPassword","Unlock","CheckLock","Disable","Enable","Info","List")]
    [string]$Action,
    
    [string]$Username,
    [string]$FirstName,
    [string]$LastName,
    [string]$Department,
    [string]$Title,
    [string]$Manager,
    [string]$Reason
)

# Import Active Directory module
Import-Module ActiveDirectory -ErrorAction Stop

$Domain = "rivi.local"
$DefaultOU = "OU=Users,DC=rivi,DC=local"
$DisabledOU = "OU=Disabled-Accounts,DC=rivi,DC=local"

function Write-Color {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Pass { Write-Color "[PASS] $args" "Green" }
function Write-Fail { Write-Color "[FAIL] $args" "Red" }
function Write-Info { Write-Color "[INFO] $args" "Cyan" }
function Write-Warn { Write-Color "[WARN] $args" "Yellow" }

Write-Color "=" * 50 "Cyan"
Write-Color "  RIVI AD User Management Script v1.0" "Green"
Write-Color "  Domain: $Domain" "Cyan"
Write-Color "=" * 50 "Cyan"

switch ($Action) {

    "Create" {
        if (-not $FirstName -or -not $LastName) {
            Write-Fail "FirstName and LastName are required for Create action"
            exit 1
        }
        
        $SamAccount = "$($FirstName.ToLower()).$($LastName.ToLower())"
        $DisplayName = "$FirstName $LastName"
        $Email = "$SamAccount@$Domain"
        $TempPassword = "Rivi@2025!"
        
        Write-Info "Creating user: $SamAccount"
        
        try {
            New-ADUser `
                -Name $DisplayName `
                -GivenName $FirstName `
                -Surname $LastName `
                -SamAccountName $SamAccount `
                -UserPrincipalName $Email `
                -EmailAddress $Email `
                -Department $Department `
                -Title $Title `
                -Path $DefaultOU `
                -AccountPassword (ConvertTo-SecureString $TempPassword -AsPlainText -Force) `
                -ChangePasswordAtLogon $true `
                -Enabled $true
            
            Write-Pass "User created: $SamAccount"
            Write-Info "Email: $Email"
            Write-Info "Temp Password: $TempPassword (user must change on first login)"
            
            # Add to default groups
            Add-ADGroupMember -Identity "Domain Users" -Members $SamAccount -ErrorAction SilentlyContinue
            Write-Pass "Added to Domain Users group"
            
        } catch {
            Write-Fail "Failed to create user: $_"
        }
    }

    "ResetPassword" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        
        $TempPassword = "TempPass@$(Get-Date -Format 'MMdd')!"
        
        try {
            $User = Get-ADUser -Identity $Username -Properties DisplayName, Department, PasswordLastSet
            Write-Info "User found: $($User.DisplayName) ($($User.Department))"
            Write-Info "Last password change: $($User.PasswordLastSet)"
            
            Set-ADAccountPassword -Identity $Username `
                -NewPassword (ConvertTo-SecureString $TempPassword -AsPlainText -Force) `
                -Reset
            
            Set-ADUser -Identity $Username -ChangePasswordAtLogon $true
            
            Write-Pass "Password reset successful!"
            Write-Color "New temp password: $TempPassword" "Yellow"
            Write-Warn "User MUST change password on next login"
        } catch {
            Write-Fail "Password reset failed: $_"
        }
    }

    "CheckLock" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        
        try {
            $User = Get-ADUser -Identity $Username -Properties `
                LockedOut, BadLogonCount, BadPasswordTime, LockedOut, `
                AccountLockoutTime, DisplayName, Enabled, LastLogonDate
            
            Write-Info "User: $($User.DisplayName)"
            Write-Info "Account Enabled: $($User.Enabled)"
            Write-Info "Account Locked: $($User.LockedOut)"
            Write-Info "Bad Password Count: $($User.BadLogonCount)"
            Write-Info "Last Bad Password: $($User.BadPasswordTime)"
            Write-Info "Lockout Time: $($User.AccountLockoutTime)"
            Write-Info "Last Successful Login: $($User.LastLogonDate)"
            
            if ($User.LockedOut) {
                Write-Warn "Account IS locked. Run with -Action Unlock to unlock."
            } else {
                Write-Pass "Account is NOT locked."
            }
        } catch {
            Write-Fail "User not found: $_"
        }
    }

    "Unlock" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        
        try {
            $User = Get-ADUser -Identity $Username -Properties LockedOut, DisplayName
            
            if (-not $User.LockedOut) {
                Write-Warn "Account $Username is not locked — nothing to unlock"
                exit 0
            }
            
            Unlock-ADAccount -Identity $Username
            Write-Pass "Account unlocked: $($User.DisplayName)"
            Write-Info "Advise user: Check Caps Lock, verify correct password"
        } catch {
            Write-Fail "Unlock failed: $_"
        }
    }

    "Disable" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        $DisableReason = if ($Reason) { $Reason } else { "Disabled on $(Get-Date -Format 'yyyy-MM-dd')" }
        
        try {
            $User = Get-ADUser -Identity $Username -Properties DisplayName, MemberOf
            
            # Remove from all groups except Domain Users
            foreach ($Group in $User.MemberOf) {
                $GroupName = (Get-ADGroup $Group).SamAccountName
                if ($GroupName -ne "Domain Users") {
                    Remove-ADGroupMember -Identity $Group -Members $Username -Confirm:$false
                    Write-Info "Removed from group: $GroupName"
                }
            }
            
            # Disable account
            Disable-ADAccount -Identity $Username
            
            # Update description
            Set-ADUser -Identity $Username -Description "DISABLED: $DisableReason"
            
            Write-Pass "Account disabled: $($User.DisplayName)"
            Write-Pass "Removed from all security groups"
            Write-Pass "Description updated with disable reason"
            Write-Warn "Move to Disabled OU manually or run Move action"
        } catch {
            Write-Fail "Disable failed: $_"
        }
    }

    "Enable" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        
        try {
            Enable-ADAccount -Identity $Username
            Set-ADUser -Identity $Username -ChangePasswordAtLogon $true
            Write-Pass "Account enabled: $Username"
            Write-Info "User must set new password on first login"
        } catch {
            Write-Fail "Enable failed: $_"
        }
    }

    "Info" {
        if (-not $Username) { Write-Fail "Username required"; exit 1 }
        
        try {
            $User = Get-ADUser -Identity $Username -Properties *
            
            Write-Color "`nUser Details:" "Cyan"
            Write-Info "Display Name:      $($User.DisplayName)"
            Write-Info "Username:          $($User.SamAccountName)"
            Write-Info "Email:             $($User.EmailAddress)"
            Write-Info "Department:        $($User.Department)"
            Write-Info "Title:             $($User.Title)"
            Write-Info "Enabled:           $($User.Enabled)"
            Write-Info "Locked:            $($User.LockedOut)"
            Write-Info "Password Expires:  $($User.PasswordNeverExpires)"
            Write-Info "Last Login:        $($User.LastLogonDate)"
            Write-Info "Created:           $($User.Created)"
            
            Write-Color "`nGroup Memberships:" "Cyan"
            Get-ADPrincipalGroupMembership $Username | ForEach-Object { Write-Info "  - $($_.Name)" }
        } catch {
            Write-Fail "User not found: $_"
        }
    }

    "List" {
        Write-Color "`nAll Active Directory Users:" "Cyan"
        Get-ADUser -Filter * -Properties Department, Enabled, LastLogonDate | `
            Select-Object SamAccountName, DisplayName, Department, Enabled, LastLogonDate | `
            Sort-Object DisplayName | `
            Format-Table -AutoSize
    }
}

Write-Color "`nScript completed. | RIVI Enterprises" "Cyan"
