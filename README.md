# 🖥️ IT Support Practical Portfolio — L1 / L2 / L3

A hands-on portfolio of 7 IT support and security projects, built and documented entirely on a self-hosted VMware lab consisting of a Windows Server 2019 domain controller, a Windows 11 Pro client, and a Kali Linux host.

Every project follows the same structure: problem statement → step-by-step resolution with real commands → screenshot evidence → resolution summary, the same way a real support ticket or incident report would be documented.

## 🖥️ Lab Environment (used across all projects)

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 | Domain Controller / DNS / DHCP | `192.168.100.10` |
| Windows 11 Pro | Domain-Joined Client | `192.168.100.25` |
| Kali Linux | Diagnostics / Security Testing Host | `192.168.100.102` |

**Domain:** `corp.local` | **Hypervisor:** VMware Workstation Pro

## 📁 Projects

| # | Project | Level | Skills Demonstrated |
|---|---|---|---|
| 01 | [Network Troubleshooting](./01-network-troubleshooting) | L1 | DNS/DHCP diagnosis, ping/tracert, cross-platform verification |
| 02 | [Windows OS Support](./02-windows-os-support) | L1 | Task Manager, Event Viewer, Services, Safe Mode, local users |
| 03 | [Linux Administration](./03-linux-administration) | L1/L2 | SSH, sudo, UFW firewall, cron, auth log analysis |
| 04 | [Active Directory Lab](./04-active-directory-lab) | L2 | OU design, user lifecycle, domain join, lockout recovery |
| 05 | [DNS & DHCP Infrastructure](./05-dns-dhcp-infrastructure) | L2 | A/CNAME records, DHCP scopes & reservations |
| 06 | [Group Policy Management](./06-group-policy-management) | L2 | Password policy, USB blocking, drive mapping via GPO |
| 07 | [Security Incident Response](./07-security-incident-response) | L3 | Brute-force detection, log analysis, containment, IR reporting |

## 🎯 Why This Portfolio

Most junior IT/security candidates list certifications and tool names with no proof of hands-on capability. Every claim in this portfolio is backed by an actual command run on an actual machine, with a screenshot to prove it. The structure mirrors real workplace documentation — ticket notes, runbooks, and incident reports — not just tutorial-following.

## 🔗 Links

- 💼 Resume: see [`RESUME_BULLETS.md`](./RESUME_BULLETS.md) for ready-to-use bullet points
- 📱 LinkedIn: see [`LINKEDIN_POSTS.md`](./LINKEDIN_POSTS.md) for post templates
- 📤 Upload guide: see [`GIT_UPLOAD_GUIDE.md`](./GIT_UPLOAD_GUIDE.md) for step-by-step Git instructions

---
<sub>Built and documented by Rithika.U · Chennai, India</sub>
