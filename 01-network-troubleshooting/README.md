# 🌐 Network Troubleshooting Lab — 3-Tier VM Environment

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L1%2FL2-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project documents systematic network troubleshooting performed across a 3-VM lab environment simulating a real corporate network: a Windows Server 2019 domain controller, a Windows 11 client, and a Kali Linux host. The goal was to diagnose and resolve common connectivity issues — DNS failures, DHCP misconfiguration, and gateway unreachability — using the same diagnostic workflow an L1/L2 IT support engineer follows on a live helpdesk ticket.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 | Domain Controller / DNS / DHCP | `192.168.100.10` |
| Windows 11 Pro | Client Workstation | `192.168.100.20` |
| Kali Linux | Network Diagnostics Host | `192.168.100.102` |

**Hypervisor:** VMware Workstation Pro
**Network Mode:** Custom (VMnet) — all 3 VMs on the same `/24` subnet

## 🎯 Objectives

- Diagnose "no internet" and "cannot reach server" scenarios using a structured checklist
- Verify IP configuration, gateway reachability, and DNS resolution across Windows and Linux clients
- Identify the exact OSI layer where a fault occurs before escalating
- Document each finding the way a ticket would be documented for a supervisor or L2 engineer

## 🔧 Tools & Commands Used

`ipconfig` `ping` `nslookup` `tracert` `netsh` `ip a` `dig` `traceroute`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — Baseline IP Configuration Check (Windows 11)

Opened Command Prompt on the Windows 11 client and pulled the full network configuration to confirm the adapter had a valid lease from the DHCP server.

```cmd
ipconfig /all
```

**Expected good output:** DHCP Enabled: Yes, valid IPv4 address in the `192.168.100.x` range, gateway `192.168.100.1`, DNS server `192.168.100.10`.

📸 *Screenshot: `01-ipconfig-all-output.png`*

---

### Step 2 — Gateway Reachability Test

Confirmed the client could reach its default gateway before testing anything further out.

```cmd
ping 192.168.100.1
```

A successful reply here confirms the local network segment is healthy and isolates the problem to either DNS or upstream routing if later steps fail.

📸 *Screenshot: `02-ping-gateway-success.png`*

---

### Step 3 — Domain Controller Connectivity Test

Verified Layer 3 reachability to the Windows Server 2019 box, since DNS and authentication both depend on this path being open.

```cmd
ping 192.168.100.10
```

📸 *Screenshot: `03-ping-domain-controller.png`*

---

### Step 4 — DNS Resolution Test

Tested whether the client could resolve the internal domain name, distinguishing a pure connectivity issue from a DNS-specific issue.

```cmd
nslookup corp.local
nslookup corp.local 192.168.100.10
```

📸 *Screenshot: `04-nslookup-dns-test.png`*

---

### Step 5 — Cross-Platform Verification (Kali Linux)

Repeated the same checks from the Kali Linux VM to confirm the issue (or the fix) was consistent across operating systems, not specific to Windows networking stack quirks.

```bash
ip a
ping -c 4 192.168.100.10
dig @192.168.100.10 company.local
```

📸 *Screenshot: `05-kali-network-verification.png`*

---

### Step 6 — Route Tracing

When a remote host was unreachable, traced the path hop-by-hop to identify exactly where the route broke.

```cmd
tracert google.com
```
```bash
traceroute 8.8.8.8
```

📸 *Screenshot: `06-tracert-route-path.png`*

---

### Step 7 — DNS Cache Reset & Lease Renewal (Resolution)

Where stale DNS data was the root cause, cleared the resolver cache and forced a new DHCP lease.

```cmd
ipconfig /flushdns
ipconfig /release
ipconfig /renew
ipconfig /registerdns
```

📸 *Screenshot: `07-flushdns-renew-fix-applied.png`*

---

## ✅ Resolution Summary

| Symptom | Root Cause | Fix Applied |
|---|---|---|
| Client showed `169.254.x.x` address | DHCP server unreachable / lease expired | `ipconfig /release` → `/renew` restored valid lease |
| Internal hostnames not resolving | Stale DNS cache on client | `ipconfig /flushdns` + `/registerdns` |
| `ping 8.8.8.8` worked, `ping google.com` failed | DNS-specific failure, not connectivity | Confirmed via `nslookup` against external vs internal DNS server |

## 📚 What This Demonstrates

- Methodical, layer-by-layer troubleshooting rather than guesswork
- Comfort working across both Windows and Linux command-line tools
- Ability to isolate root cause before applying a fix — not just restarting things randomly
- Documentation discipline suitable for ticketing systems (ServiceNow, Jira Service Management)

## 🗂️ Folder Structure

```
01-network-troubleshooting/
├── README.md
└── screenshots/
    ├── 01-ipconfig-all-output.png
    ├── 02-ping-gateway-success.png
    ├── 03-ping-domain-controller.png
    ├── 04-nslookup-dns-test.png
    ├── 05-kali-network-verification.png
    ├── 06-tracert-route-path.png
    └── 07-flushdns-renew-fix-applied.png
```

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*
