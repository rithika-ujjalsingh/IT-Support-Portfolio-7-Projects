# 🐧 Linux Server Administration Lab — Kali Linux

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L1%2FL2-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project demonstrates core Linux server administration skills performed on a Kali Linux VM configured to behave like a production Linux server — user management, SSH access, service control, firewall configuration, and log analysis. These are the exact skills tested in IT support and junior sysadmin interviews.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Kali Linux | Linux Server (admin practice) | `192.168.100.102` |
| Windows 11 Pro | SSH Client (for remote access test) | `192.168.100.20` |

**Hypervisor:** VMware Workstation Pro

## 🎯 Objectives

- Install and enable OpenSSH server for remote administration
- Create a new user with sudo privileges and verify elevated access
- Configure UFW firewall to allow only required ports
- Schedule a recurring task using cron
- Analyze authentication logs for failed/successful login attempts
- Practice file permission management (`chmod`, `chown`)

## 🔧 Tools & Commands Used

`apt` `systemctl` `useradd` `usermod` `passwd` `ufw` `crontab` `journalctl` `chmod` `ss`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Install & Enable SSH Server

```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl start ssh
sudo systemctl enable ssh
sudo systemctl status ssh
```

📸 *Screenshot: `01-ssh-server-status-active.png`*

---

### Step 2 — Create User with Sudo Privileges

```bash
sudo useradd -m -s /bin/bash novauser
sudo passwd novauser
sudo usermod -aG sudo novauser
```

Verified the new account had real elevated access, not just group membership on paper:

```bash
su - novauser
sudo whoami
```

📸 *Screenshot: `02-sudo-user-verification.png`*

---

### Step 3 — Remote SSH Login Test

Connected to the Kali "server" from the Windows 11 client to confirm SSH was reachable from another machine on the network, not just localhost.

```cmd
ssh novauser@192.168.100.102
```

📸 *Screenshot: `03-remote-ssh-login-success.png`*

---

### Step 4 — Firewall Configuration (UFW)

Locked down the server to only allow SSH (port 22) and HTTP (port 80), denying everything else by default — basic server hardening.

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw enable
sudo ufw status verbose
```

📸 *Screenshot: `04-ufw-firewall-rules-active.png`*

---

### Step 5 — Scheduled Task (Cron Job)

Set up a recurring job that simulates an automated nightly backup task.

```bash
crontab -e
# Added line:
0 2 * * * /home/kali/backup.sh
crontab -l
```

📸 *Screenshot: `05-crontab-scheduled-job.png`*

---

### Step 6 — Authentication Log Analysis

Reviewed the auth log to identify failed login attempts — the same first step taken when investigating a suspected brute-force attempt.

```bash
sudo tail -30 /var/log/auth.log
sudo grep "Failed password" /var/log/auth.log
```

📸 *Screenshot: `06-auth-log-failed-logins.png`*

---

## ✅ Resolution Summary

| Task | Action Taken | Outcome |
|---|---|---|
| Need remote access to server | Installed & enabled OpenSSH | Server accessible via SSH from another VM |
| New team member needs admin rights | Created user + added to sudo group | Verified `sudo whoami` returns root |
| Server exposed to unnecessary ports | Configured UFW to allow only 22 & 80 | Firewall verbose status confirms lockdown |
| Manual nightly backups forgotten | Scheduled cron job | Task runs automatically at 2 AM daily |

## 📚 What This Demonstrates

- Comfort administering a headless Linux server entirely from the command line
- Security-conscious defaults — only opening ports that are actually needed
- Ability to investigate authentication logs, a core blue-team/IT-security skill
- Real understanding of Linux permission and privilege models, not just memorized commands

## 🗂️ Folder Structure

```
03-linux-administration/
├── README.md
└── screenshots/
    ├── 01-ssh-server-status-active.png
    ├── 02-sudo-user-verification.png
    ├── 03-remote-ssh-login-success.png
    ├── 04-ufw-firewall-rules-active.png
    ├── 05-crontab-scheduled-job.png
    └── 06-auth-log-failed-logins.png
```

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
