# 📸 Screenshot Checklist — Active Directory Lab

| # | Filename | What to capture | VM to use |
|---|---|---|---|
| 1 | `01-ou-structure-created.png` | ADUC left pane showing HR, Finance, IT, Disabled Users OUs under company.local | Windows Server 2019 |
| 2 | `02-new-user-aduc-wizard.png` | The "New Object - User" wizard with Nova Singh's details filled in | Windows Server 2019 |
| 3 | `03-security-group-membership.png` | HR-Team group Properties → Members tab showing nova.singh listed | Windows Server 2019 |
| 4 | `04-domain-join-confirmation.png` | Windows 11 "You're all set" or restart prompt after domain join | Windows 11 |
| 5 | `05-domain-user-first-login.png` | Windows 11 lock screen showing nova.singh as an available login option, or desktop after login | Windows 11 |
| 6 | `06-account-unlock-powershell.png` | PowerShell window: `Search-ADAccount -LockedOut` then `Unlock-ADAccount` | Windows Server 2019 |
| 7 | `07-password-reset-confirmation.png` | PowerShell after running the password reset commands, no errors shown | Windows Server 2019 |
| 8 | `08-account-disabled-offboarded.png` | ADUC showing the account icon with the down-arrow (disabled) inside the Disabled Users OU | Windows Server 2019 |

## Tip

For screenshot 5, the cleanest version is the Windows lock screen showing "Other User" → typing nova.singh — it visually proves domain join without needing to show a full desktop.
