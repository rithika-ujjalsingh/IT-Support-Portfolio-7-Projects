# 📱 LinkedIn Post Templates — One Per Project

Post these one at a time, spaced a few days apart, not all together — this keeps your profile showing consistent activity over weeks instead of one burst.

---

## Post 1 — Network Troubleshooting

```
🌐 Diagnosed a simulated network outage across a 3-tier VM lab — and documented it the way I would on a real support ticket.

Setup: Windows Server 2019 (DC) + Windows 11 client + Kali Linux, all on an isolated VMware network.

The issue: client couldn't resolve internal hostnames. Walked through the full diagnostic chain — IP config → gateway reachability → DNS resolution → cross-platform verification on Linux → root cause identified as a stale DNS cache.

Full step-by-step writeup with command output and screenshots on GitHub 👇
[link to repo]

#ITSupport #Networking #WindowsServer #HelpDesk #TechSkills
```

---

## Post 2 — Windows OS Support

```
🪟 Some days the "easy" tickets are the most important ones to get right.

Practiced the core L1 Windows toolkit on a Windows 11 VM: Task Manager triage, Event Viewer log filtering, service recovery, local user provisioning, and Safe Mode boot recovery.

These are the exact skills that keep a helpdesk queue moving — full writeup and screenshots on GitHub.
[link to repo]

#WindowsSupport #L1Support #ITHelpdesk #SysAdmin
```

---

## Post 3 — Linux Administration

```
🐧 Configured a Kali Linux box to behave like a production Linux server — not just a pentesting distro.

✅ SSH server setup + remote access verification
✅ Sudo-privileged user provisioning
✅ UFW firewall lockdown (only required ports open)
✅ Scheduled cron jobs
✅ Auth log analysis for failed login attempts

Full command-by-command breakdown on GitHub:
[link to repo]

#Linux #SysAdmin #CyberSecurity #OpenSSH #ITSupport
```

---

## Post 4 — Active Directory Lab

```
🗂️ Active Directory isn't just "create a user" — it's a full lifecycle.

Built out a department-based OU structure, created and grouped users, joined a Windows 11 client to the domain, then simulated and resolved an account lockout and a password reset entirely via PowerShell — finishing with a proper offboarding workflow (disable + archive, never just delete).

Step-by-step with PowerShell snippets and screenshots:
[link to repo]

#ActiveDirectory #PowerShell #WindowsServer #ITSupport #SysAdmin
```

---

## Post 5 — DNS & DHCP Infrastructure

```
🔍 DNS and DHCP are the two services nobody notices — until they break.

Configured both from scratch on Windows Server 2019: A/CNAME records, reverse lookup zones, DHCP scopes with exclusion ranges, and a MAC-based reservation — then verified every piece of it from both a Windows and a Linux client.

Full configuration walkthrough on GitHub:
[link to repo]

#DNS #DHCP #NetworkInfrastructure #WindowsServer #ITSupport
```

---

## Post 6 — Group Policy Management

```
📋 One GPO link can change security posture for an entire domain — here's how I tested that hands-on.

Built and enforced four policies on a Windows Server 2019 domain: password complexity, auto screen-lock, removable storage blocking, and automatic network drive mapping — then verified every single one actually applied using gpresult.

Full writeup + screenshots:
[link to repo]

#GroupPolicy #WindowsServer #ITSecurity #SysAdmin
```

---

## Post 7 — Security Incident Response

```
🛡️ Simulated a brute-force attack against my own lab — then ran the full incident response playbook against it.

Isolated VMware lab, Kali Linux as the attacker, Windows 11 as the target:
1️⃣ Simulated the attack
2️⃣ Detected it via Windows Security Event Logs (Event ID 4625)
3️⃣ Contained it with account lockout policy + host firewall IP block
4️⃣ Verified containment and wrote up the incident like a real SOC report

Full disclaimer: strictly an isolated lab I own, used only for skill-building. Writeup on GitHub:
[link to repo]

#CyberSecurity #IncidentResponse #BlueTeam #SOC #EthicalHacking
```

---

## Profile Headline Suggestions

Pick one that matches where you're applying:

```
IT Support Engineer (L1/L2) | Active Directory | Windows Server | Networking | Building hands-on lab portfolio
```
```
Aspiring SOC Analyst | Incident Response | Windows & Linux Administration | Hands-on VMware Lab Builder
```
```
IT Engineer transitioning into Cybersecurity | AD, GPO, DNS/DHCP, Linux Admin | 7-project lab portfolio on GitHub
```

## About Section Template

```
I build and document hands-on IT support and security labs to develop real, demonstrable
skills — not just certificates.

My self-hosted VMware lab (Windows Server 2019, Windows 11, Kali Linux) is where I practice
everything from L1 network troubleshooting to L3 incident response: Active Directory
administration, Group Policy enforcement, DNS/DHCP configuration, Linux server hardening,
and security incident detection & containment.

Every project is fully documented on GitHub with step-by-step methodology, real command
output, and screenshot evidence — github.com/rithisingh2020

Currently focused on: IT support engineering roles with a path toward cybersecurity / SOC analyst work.
```

---
*Posting cadence tip: 1 post every 3–4 days keeps your activity feed looking consistent without flooding connections' feeds.*
