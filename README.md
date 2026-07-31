<p align="center">
  <img src="./assets/portfolio-banner.png" width="100%" alt="IT Support Portfolio Banner">
</p>

<h1 align="center">🖥️ IT Support Practical Portfolio — L1 / L2 / L3</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Platform-VMware-blue" alt="Platform">
  <img src="https://img.shields.io/badge/Projects-13-orange" alt="Projects">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

<p align="center">
A hands-on portfolio of 13 IT support and cybersecurity projects, built and documented entirely on a self-hosted VMware lab consisting of a Windows Server 2019 domain controller, a Windows 11 Pro client, and a Kali Linux host.
</p>

<p align="center">
Every project follows the same structure: problem statement → step-by-step resolution with real commands → screenshot evidence → resolution summary — the same way a real support ticket or incident report would be documented.
</p>

> This repo is kept focused on IT Support (L1/L2/L3) work specifically. Offensive-security / red-team projects live in separate repos on this profile.

---

## 📚 Table of Contents

- [Lab Environment](#-lab-environment-used-across-most-projects)
- [Skills Demonstrated](#-skills-demonstrated)
- [Project Roadmap](#-project-roadmap)
- [Repository Structure](#-repository-structure)
- [Projects](#-projects)
- [Technologies Used](#-technologies-used)
- [Key Achievements](#-key-achievements)
- [Learning Outcomes](#-learning-outcomes)
- [Future Enhancements](#-future-enhancements)
- [Links](#-links)
- [Support](#-support)
- [License](#-license)

---

## 🖥️ Lab Environment (used across most projects)

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 (DC01) | Domain Controller / DNS / DHCP | `192.168.100.10` |
| Windows 11 Pro (CORP-PC01) | Domain-Joined Client | `192.168.100.25` |
| Kali Linux | Diagnostics / Security Testing Host | `192.168.100.102` |

**Domain:** `corp.local` &nbsp;|&nbsp; **DHCP Range:** `192.168.100.100 – 192.168.100.200` &nbsp;|&nbsp; **Hypervisor:** VMware Workstation Pro

---

## 🛠 Skills Demonstrated

- Windows 11 Administration
- Windows Server 2019
- Active Directory
- Group Policy
- DNS & DHCP
- PowerShell Scripting
- VMware Workstation Pro
- Linux Administration (Kali)
- Bash Scripting
- Python Automation
- Event Viewer / Log Analysis
- Network Troubleshooting
- TCP/IP Fundamentals
- Security Incident Response
- Security Hardening (Firewall, UFW, GPO)
- Technical Documentation

---

## 🗺 Project Roadmap

| Project | Status |
|---|---|
| 01 — Network Troubleshooting | ✅ Completed |
| 02 — Windows OS Support | ✅ Completed |
| 03 — Linux Administration | ✅ Completed |
| 04 — Active Directory Lab | ✅ Completed |
| 05 — DNS & DHCP Infrastructure | ✅ Completed |
| 06 — Group Policy Management | ✅ Completed |
| 07 — Security Incident Response | ✅ Completed |
| 08 — IT Support Ticketing System | ✅ Completed |
| 09 — Network Diagnostics Toolkit | ✅ Completed |
| 10 — AD User Management Scripts | ✅ Completed |
| 11 — Windows Server Lab Setup | ✅ Completed |
| 12 — Security Incident Response Playbook | ✅ Completed |
| 13 — SIEM Log Analysis Tool | ✅ Completed |

---

## 🗂 Repository Structure

```
IT-Support-Portfolio-Projects/
├── 01-network-troubleshooting
├── 02-windows-os-support
├── 03-linux-administration
├── 04-active-directory-lab
├── 05-dns-dhcp-infrastructure
├── 06-group-policy-management
├── 07-security-incident-response
├── 08-it-support-ticketing-system
├── 09-network-diagnostics-toolkit
├── 10-ad-user-management-scripts
├── 11-windows-server-lab-setup
├── 12-security-incident-response-playbook
├── 13-siem-log-analysis-tool
├── assets/                  → banner image, misc graphics
├── GIT_UPLOAD_GUIDE.md
├── LINKEDIN_POSTS.md
├── RESUME_BULLETS.md
├── LICENSE
└── README.md
```

---

## 📁 Projects

### Core Support & Infrastructure (01–07)

| # | Project | Level | Skills Demonstrated |
|---|---|---|---|
| 01 | [Network Troubleshooting](./01-network-troubleshooting) | L1 | Layer-by-layer diagnosis of DNS/DHCP/gateway failures across Windows + Linux clients; resolved a stale-DNS-cache root cause |
| 02 | [Windows OS Support](./02-windows-os-support) | L1 | Task Manager triage, Event Viewer log filtering, Print Spooler service recovery, local user provisioning, Safe Mode boot |
| 03 | [Linux Administration](./03-linux-administration) | L1/L2 | SSH server hardening, sudo-privileged user setup, UFW firewall lockdown, cron scheduling, auth log analysis |
| 04 | [Active Directory Lab](./04-active-directory-lab) | L2 | OU design, GUI + PowerShell user creation, security group membership, domain join, account lockout recovery, password reset, offboarding |
| 05 | [DNS & DHCP Infrastructure](./05-dns-dhcp-infrastructure) | L2 | A/CNAME records, reverse lookup zones, DHCP scope + MAC-based reservation, cross-platform DNS verification |
| 06 | [Group Policy Management](./06-group-policy-management) | L2 | Password policy, screen-lock, USB-block, and drive-mapping GPOs, verified via Group Policy Modeling Wizard |
| 07 | [Security Incident Response](./07-security-incident-response) | L3 | Simulated SSH brute-force (Hydra), detected via Event ID 4625, contained with account lockout + firewall IP block |

### Automation & Tooling (08–13)

| # | Project | Level | Skills Demonstrated |
|---|---|---|---|
| 08 | [IT Support Ticketing System](./08-it-support-ticketing-system) | L1 | Python CLI ticketing tool — priority/SLA tagging, escalation logic, JSON database, audit log |
| 09 | [Network Diagnostics Toolkit](./09-network-diagnostics-toolkit) | L1/L2 | Python tool automating ping/traceroute/DNS/port-scan into a single HTML report |
| 10 | [AD User Management Scripts](./10-ad-user-management-scripts) | L2 | PowerShell scripts for user creation, password reset, unlock, disable/offboard, bulk CSV import, audit reporting |
| 11 | [Windows Server Lab Setup](./11-windows-server-lab-setup) | L2 | Fully scripted domain controller build — AD DS promotion, DNS, DHCP, OUs, baseline GPO |
| 12 | [Security Incident Response Playbook](./12-security-incident-response-playbook) | L3 | 4 IR playbooks (account compromise, phishing, ransomware, insider threat) mapped to MITRE ATT&CK, with simulation labs |
| 13 | [SIEM Log Analysis Tool](./13-siem-log-analysis-tool) | L3 | Python SIEM-style log parser detecting brute-force, lockouts, and after-hours logins; HTML dashboards; Windows→Kali log forwarding |

---

## 💻 Technologies Used

**Operating Systems**
Windows Server 2019 · Windows 11 Pro · Kali Linux

**Microsoft Technologies**
Active Directory · Group Policy · DNS · DHCP · PowerShell

**Networking**
TCP/IP · DNS · DHCP · ICMP · Routing & Traceroute

**Security**
Event Viewer · Windows Firewall · Hydra · MITRE ATT&CK · UFW

**Virtualization**
VMware Workstation Pro

**Languages**
Python · PowerShell · Bash

---

## 🎯 Key Achievements

✔ Completed 13 practical IT Support labs across L1, L2, and L3 difficulty levels
✔ Built and administered a full enterprise-style Active Directory environment (OUs, users, groups, GPOs)
✔ Automated repetitive administrative tasks with PowerShell (bulk user creation, audit reporting, lockout recovery)
✔ Developed Python-based IT support tools (ticketing system, network diagnostics, SIEM log analyzer)
✔ Documented every lab with real command output, screenshots, and resolution summaries
✔ Simulated and contained a real-world-style brute-force security incident end-to-end
✔ Applied consistent, industry-standard troubleshooting methodology (OSI-layer approach) across all network issues

---

## 📖 Learning Outcomes

This portfolio strengthened practical skills in:

- Enterprise Windows Administration
- Active Directory Management
- Windows & Linux Troubleshooting
- Network Diagnostics
- Security Monitoring & Incident Response
- IT Documentation & Ticket Writing
- Automation using Python
- PowerShell Scripting

---

## 🚀 Future Enhancements

Planned additions to keep building on this foundation:

- WSUS (Windows Server Update Services)
- Microsoft Intune
- Microsoft Defender for Endpoint
- Azure Active Directory / Entra ID
- Microsoft Sentinel
- Wazuh / Splunk
- SCCM
- Ansible

---

## 🔗 Links

- 💼 Resume bullets: [`RESUME_BULLETS.md`](./RESUME_BULLETS.md)
- 📱 LinkedIn post templates: [`LINKEDIN_POSTS.md`](./LINKEDIN_POSTS.md)
- 📤 Git upload guide: [`GIT_UPLOAD_GUIDE.md`](./GIT_UPLOAD_GUIDE.md)
- 🔗 GitHub profile: [github.com/rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)

---

## ⚠️ Disclaimer

All testing (including simulated brute-force and incident-response exercises) was performed exclusively within an isolated VMware lab that I own and control. No external or third-party systems were targeted at any point.

---

## 🤝 Support

If you found this portfolio useful, consider giving it a ⭐.
Feedback and suggestions are always welcome — feel free to open an issue or connect on LinkedIn.

---

## 📄 License

Licensed under the [MIT License](./LICENSE).

---

<p align="center">

Built with ❤️ by <strong>Rithika U</strong>

BE Computer Science Engineering

IT Support • Windows Administration • Active Directory • Cybersecurity

Chennai, India

</p>
