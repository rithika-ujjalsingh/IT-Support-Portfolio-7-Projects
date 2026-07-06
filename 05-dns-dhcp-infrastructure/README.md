# 🔍 DNS & DHCP Infrastructure Configuration

[![Status](https://img.shields.io/badge/Status-Completed-success)]()
[![Level](https://img.shields.io/badge/Level-L2-blue)]()
[![Platform](https://img.shields.io/badge/Platform-VMware-orange)]()

## 📌 Project Overview

This project covers configuring and troubleshooting the two services every corporate network depends on silently: DNS (name resolution) and DHCP (automatic IP assignment). Both were configured on a Windows Server 2019 domain controller and validated from both a Windows 11 client and a Kali Linux host to confirm cross-platform reliability.

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Windows Server 2019 (DC01) | DNS Server + DHCP Server | `192.168.100.10` |
| Windows 11 Pro | DHCP/DNS Client | `192.168.100.25` (static) |
| Kali Linux | DNS Verification Host | `192.168.100.102` |

**Hypervisor:** VMware Workstation Pro
**Domain:** `corp.local`

## 🎯 Objectives

- Create and verify A, CNAME, and reverse lookup DNS records
- Configure a DHCP scope and review its address pool range
- Create a DHCP reservation so a specific device always gets the same IP
- Validate DNS resolution from both Windows and Linux clients
- Test client-side DHCP lease renewal

## 🔧 Tools & Commands Used

`DNS Manager` `DHCP Manager` `nslookup` `dig` `host` `ipconfig`

---

## 📋 Step-by-Step Walkthrough

### Step 1 — DNS A Record Creation

DNS Manager → Forward Lookup Zones → corp.local → New Host (A)
Name: webserver   IP: 192.168.100.50

📸 *Screenshot: `01-dns-a-record-created.png`*

---

### Step 2 — DNS Resolution Test from Windows 11

```cmd
nslookup webserver.corp.local
```

📸 *Screenshot: `02-nslookup-resolution-success.png`*

---

### Step 3 — CNAME (Alias) Record

DNS Manager → New Alias (CNAME)
Alias: www   FQDN: webserver.corp.local

📸 *Screenshot: `03-cname-alias-created.png`*

---

### Step 4 — Reverse Lookup Zone

Verified the reverse lookup zone (`100.168.192.in-addr.arpa`) was Active Directory-integrated and running, enabling reverse DNS (IP-to-hostname) lookups.

📸 *Screenshot: `04-reverse-lookup-zone-created.png`*

---

### Step 5 — DNS Verification from Kali Linux

Cross-platform validation that DNS responses are identical regardless of client OS.

```bash
dig @192.168.100.10 corp.local ANY
host webserver.corp.local 192.168.100.10
```

> **Troubleshooting note:** Initial `dig` queries timed out. Root cause was the same VM network adapter mismatch encountered in the Linux Administration lab — the Kali VM had reverted to the default NAT network after a restart. Re-applied the static IP on the correct virtual network, verified with `ping`, and DNS queries succeeded.

📸 *Screenshot: `05-kali-dig-dns-verification.png`*

---

### Step 6 — DHCP Scope Review

Reviewed the existing DHCP scope's address pool configuration.

DHCP Manager → Scope [192.168.100.0] → Address Pool
Range: 192.168.100.100 – 192.168.100.200

📸 *Screenshot: `06-dhcp-scope-configuration.png`*

---

### Step 7 — DHCP Reservation

Created a DHCP reservation so a specific client always receives the same IP address regardless of lease renewals — useful for devices like printers or servers that need a predictable address.

DHCP Manager → Reservations → New Reservation

IP: 192.168.100.30   MAC: (from Windows 11 ipconfig /all physical address)

📸 *Screenshot: `07-dhcp-reservation-created.png`*

---

### Step 8 — Client-Side DHCP Renewal Test

```cmd
ipconfig /release
ipconfig /renew
ipconfig /all
```

> **Testing note:** The client adapter was temporarily switched from its static IP to DHCP to test lease renewal. Because the adapter was on the NAT virtual network at the time, it received a lease from VMware's own NAT DHCP service rather than the AD-integrated DHCP server — a good illustration of why the underlying virtual network matters even when the configuration on the server side is correct. The static IP was restored afterward to preserve domain connectivity.

📸 *Screenshot: `08-dhcp-renewal-confirmation.png`*

---

## ✅ Resolution Summary

| Task | Configuration | Verification Method |
|---|---|---|
| Internal hostname needed to resolve to an IP | Created A record | `nslookup` from Windows + `dig`/`host` from Linux both returned correct IP |
| Friendly alias needed for a server | Created CNAME pointing to A record | Resolved correctly to the same final IP |
| Reverse lookups needed for logging/troubleshooting | Verified AD-integrated reverse zone | Zone confirmed running and DNSSEC-aware |
| Devices need automatic IP assignment | Reviewed DHCP scope address pool | Range confirmed (192.168.100.100–200) |
| A device needs a permanently fixed IP | Created DHCP reservation by MAC address | Reservation listed and bound to correct IP |

## 📚 What This Demonstrates

- Full ownership of core network infrastructure services, not just "how to use" them as a client
- Real network troubleshooting — diagnosing a VM connectivity issue rather than assuming DNS was misconfigured
- Cross-platform validation discipline — never assuming Windows-only testing is sufficient
- Understanding of how virtual network topology can affect service testing independent of server-side configuration

## 🗂️ Folder Structure

05-dns-dhcp-infrastructure/
├── README.md
└── screenshots/
├── 01-dns-a-record-created.png
├── 02-nslookup-resolution-success.png
├── 03-cname-alias-created.png
├── 04-reverse-lookup-zone-created.png
├── 05-kali-dig-dns-verification.png
├── 06-dhcp-scope-configuration.png
├── 07-dhcp-reservation-created.png
└── 08-dhcp-renewal-confirmation.png

---
*Part of a 7-project IT Support (L1/L2/L3) practical portfolio — built on a self-hosted VMware lab.*

