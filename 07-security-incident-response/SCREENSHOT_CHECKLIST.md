# 📸 Screenshot Checklist — Security Incident Response

| # | Filename | What to capture | VM to use |
|---|---|---|---|
| 1 | `01-hydra-bruteforce-simulation.png` | Kali terminal showing hydra running against the target | Kali Linux |
| 2 | `02-event-4625-failed-logons.png` | PowerShell output of the Get-WinEvent 4625 query showing multiple entries | Windows 11 |
| 3 | `03-account-lockout-policy-config.png` | GPO editor showing lockout threshold = 5, duration = 30 min | Windows Server 2019 |
| 4 | `04-account-lockout-triggered.png` | PowerShell `Search-ADAccount -LockedOut` showing the locked account | Windows Server 2019 |
| 5 | `05-firewall-ip-block-rule.png` | PowerShell after running New-NetFirewallRule, no errors | Windows 11 |
| 6 | `06-attacker-blocked-confirmation.png` | Kali terminal showing `ping 192.168.100.20` timing out | Kali Linux |

## ⚠️ Important safety note before recording this one

- Only ever run hydra/brute-force tools against machines you own, inside an isolated lab network with no internet bridging
- Never point these tools at any real, internet-facing, or third-party system
- When you post this on LinkedIn/GitHub, keep the disclaimer line from the README visible — recruiters and compliance-minded hiring managers specifically look for this kind of responsible framing from junior security candidates
