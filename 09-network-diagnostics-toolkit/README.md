# Network Diagnostics Toolkit — L1/L2 Practical Lab

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![Level](https://img.shields.io/badge/Level-L1%20L2%20IT%20Support-0096FF?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20Kali%20Linux-1a1a2e?style=for-the-badge)

> Automated network diagnostics tool for IT Support Engineers. Runs ping, traceroute, DNS lookup, port scan, and generates a full HTML diagnostic report — from both Windows 11 and Kali Linux.

---

## Overview

When a user says "internet is not working" or "I cannot reach the server," this tool runs a complete network diagnostic in one command and generates a shareable HTML report.

**VM Setup Used:**
- Windows 11 Client: `192.168.100.102`
- Windows Server 2019: `192.168.100.10`
- Kali Linux: `192.168.100.20`

**What you will learn:**
- Network troubleshooting methodology (OSI Layer approach)
- Python socket and subprocess usage
- Cross-platform compatibility (Windows and Linux commands)
- Automated report generation
- DNS resolution troubleshooting
- Port connectivity checking

---

## Features

| Feature | Description |
|---------|-------------|
| Ping Test | ICMP connectivity test with packet loss % |
| Traceroute | Hop-by-hop path analysis |
| DNS Lookup | Forward and reverse resolution |
| Port Scanner | Check if specific ports are open |
| Speed Test | Basic bandwidth estimation |
| HTML Report | Auto-generated shareable diagnostic report |
| Multi-Target | Test multiple hosts in one run |
| Auto-Detect OS | Uses correct commands for Windows or Linux |

---

## Prerequisites

### On Windows 11 VM (192.168.100.102)

```powershell
# Step 1: Open PowerShell as Administrator

# Step 2: Check Python
python --version
# Must be 3.10 or higher

# Step 3: Install dependencies
pip install requests colorama jinja2

# Step 4: Allow ICMP through firewall (for ping tests)
netsh advfirewall firewall add rule name="Allow ICMP" protocol=icmpv4:8,any dir=in action=allow

# Step 5: Verify network tools are available
ping 8.8.8.8
# Should show replies from 8.8.8.8

tracert 8.8.8.8
# Should show hops to Google DNS

nslookup google.com
# Should show IP addresses
```

### On Kali Linux VM (192.168.100.20)

```bash
# Step 1: Open Terminal

# Step 2: Install required packages
sudo apt update
sudo apt install python3 python3-pip traceroute dnsutils nmap -y

# Step 3: Install Python libraries
pip3 install requests colorama jinja2

# Step 4: Verify tools
ping -c 4 8.8.8.8
# Should show 4 replies

traceroute 8.8.8.8
# Should show network path

nslookup google.com
# Should show DNS resolution
```

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/rithika-ujjalsingh/Network-Diagnostics-Toolkit.git
cd Network-Diagnostics-Toolkit
```

### Step 2: Install Dependencies

```bash
# Windows
pip install -r requirements.txt

# Kali Linux
pip3 install -r requirements.txt
```

### Step 3: Run Quick Test

```bash
# Windows — test connectivity to Windows Server
python network_diagnostics.py --target 192.168.100.10

# Kali Linux — test connectivity to Windows 11
python3 network_diagnostics.py --target 192.168.100.102

# Expected output:
# Starting network diagnostics for 192.168.100.10
# [PASS] Ping: 4/4 packets received, avg 1.2ms
# [PASS] DNS: Resolves correctly
# [PASS] Port 80: Open
# [PASS] Port 443: Open
# [FAIL] Port 22: Closed
# Report saved: report_20250101_090000.html
```

---

## Usage Guide

### Basic Single Target Scan

```bash
# Syntax
python network_diagnostics.py --target <IP_or_hostname>

# Examples
python network_diagnostics.py --target 192.168.100.10
python network_diagnostics.py --target google.com
python network_diagnostics.py --target 8.8.8.8
```

### Scan Multiple Targets

```bash
# Create a targets file
echo "192.168.100.10" > targets.txt
echo "192.168.100.102" >> targets.txt
echo "8.8.8.8" >> targets.txt

# Run scan against all targets
python network_diagnostics.py --targets-file targets.txt

# Expected: One HTML report covering all three targets
```

### Specify Which Ports to Check

```bash
# Check specific ports
python network_diagnostics.py --target 192.168.100.10 --ports 80,443,3389,445,22

# Common port reference:
# 22   SSH
# 80   HTTP
# 443  HTTPS
# 135  RPC (Windows)
# 139  NetBIOS
# 445  SMB (File Sharing)
# 3389 RDP (Remote Desktop)
# 53   DNS
# 67   DHCP
```

### Full Verbose Scan with Traceroute

```bash
python network_diagnostics.py --target 192.168.100.10 --verbose --traceroute

# Output will include:
# - Detailed ping statistics
# - Full traceroute hop list
# - DNS forward and reverse lookup
# - Port scan results
# - Network interface information
```

---

## Lab Exercises

### Exercise 1: Basic Connectivity Check (20 minutes)

```
Scenario: User reports "I cannot reach the file server"
Target: Windows Server 2019 at 192.168.100.10

Step 1: Run basic diagnostic from Windows 11
  python network_diagnostics.py --target 192.168.100.10

Step 2: Check ping result
  If PASS: L1 can communicate with server, issue is application-level
  If FAIL: Network connectivity problem, escalate to L2

Step 3: Run same diagnostic from Kali Linux
  python3 network_diagnostics.py --target 192.168.100.10

Step 4: Compare results from Windows 11 vs Kali Linux
  If Windows fails but Kali passes: Windows firewall or routing issue
  If both fail: Server-side or network issue

Step 5: Check RDP port specifically
  python network_diagnostics.py --target 192.168.100.10 --ports 3389
  If port 3389 closed: RDP service disabled or firewall blocking
```

### Exercise 2: DNS Troubleshooting (20 minutes)

```
Scenario: Users can ping by IP but not by hostname

Step 1: Test DNS resolution from Windows 11
  nslookup WIN-SERVER-2019
  nslookup 192.168.100.10

Step 2: Run DNS diagnostic with toolkit
  python network_diagnostics.py --target WIN-SERVER-2019 --dns-only

Step 3: If DNS fails, check DNS server configuration
  On Windows 11:
  ipconfig /all
  Look for DNS Servers line
  Should show 192.168.100.10 (your Windows Server)

Step 4: If DNS server is wrong, fix it
  netsh interface ip set dns "Ethernet" static 192.168.100.10

Step 5: Flush DNS cache and retry
  ipconfig /flushdns
  nslookup WIN-SERVER-2019
```

### Exercise 3: Network Path Analysis (25 minutes)

```
Scenario: Application is slow, need to find bottleneck

Step 1: Run traceroute from Windows 11 to Windows Server
  python network_diagnostics.py --target 192.168.100.10 --traceroute

Step 2: Identify each hop in the output
  Hop 1: Your default gateway (router)
  Hop 2: Should be Windows Server directly (same subnet)

Step 3: Check latency at each hop
  Normal: under 5ms for local network
  Slow: over 50ms — check that network device

Step 4: Run traceroute to internet
  python network_diagnostics.py --target 8.8.8.8 --traceroute

Step 5: Identify where latency increases
  Local hops should be fast
  Internet hops will have higher latency
```

---

## OSI Layer Troubleshooting Reference

```
Layer 7 Application  — Can the app connect? Test specific ports
Layer 6 Presentation — Is data being encrypted correctly? Check SSL
Layer 5 Session      — Are sessions being established? Check auth
Layer 4 Transport    — Are ports open? TCP vs UDP test
Layer 3 Network      — Can ping the IP? Routing table correct?
Layer 2 Data Link    — Can ARP resolve MAC? Check NIC drivers
Layer 1 Physical     — Is cable plugged in? NIC showing in Device Mgr?

Always troubleshoot from Layer 1 up to Layer 7.
```

---

## Project Structure

```
Network-Diagnostics-Toolkit/
|
├── network_diagnostics.py    Main script entry point
├── ping_test.py              ICMP ping implementation
├── traceroute.py             Traceroute implementation
├── dns_lookup.py             DNS resolution testing
├── port_scanner.py           TCP port connectivity check
├── report_generator.py       HTML report builder
├── requirements.txt          Python dependencies
├── templates/
│   └── report.html           Jinja2 HTML report template
├── README.md                 This documentation file
├── SECURITY.md               Security policy
└── CONTRIBUTING.md           Contribution guidelines
```

---

## Author

**Rithika U** — Cybersecurity Engineer | RIVI Enterprises
- GitHub: [@rithika-ujjalsingh](https://github.com/rithika-ujjalsingh)
- LinkedIn: [linkedin.com/in/rithika-u](https://linkedin.com/in/rithika-u)

*Built for IT Support learners | RIVI Enterprises 2025*
