# 📸 Screenshot Checklist — Linux Administration Lab

| # | Filename | What to capture | VM to use |
|---|---|---|---|
| 1 | `01-ssh-server-status-active.png` | `systemctl status ssh` showing "active (running)" in green | Kali Linux |
| 2 | `02-sudo-user-verification.png` | Terminal showing `su - novauser` then `sudo whoami` returning `root` | Kali Linux |
| 3 | `03-remote-ssh-login-success.png` | Windows cmd window showing successful SSH connection + Kali prompt | Windows 11 (client side) |
| 4 | `04-ufw-firewall-rules-active.png` | `ufw status verbose` output showing rules for ports 22 and 80 | Kali Linux |
| 5 | `05-crontab-scheduled-job.png` | `crontab -l` output showing the scheduled backup line | Kali Linux |
| 6 | `06-auth-log-failed-logins.png` | `grep "Failed password" /var/log/auth.log` with at least a few lines of output | Kali Linux |

## Tip for screenshot 6

If your auth log is empty (no failed logins yet), generate some test data first by intentionally typing a wrong SSH password 2–3 times from the Windows 11 VM, then re-run the grep command.
