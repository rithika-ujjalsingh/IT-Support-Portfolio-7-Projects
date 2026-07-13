#!/usr/bin/env python3
"""
Network Diagnostics Toolkit — L1/L2 Practical Lab
Author: Rithika U | RIVI Enterprises
"""

import subprocess
import socket
import sys
import os
import platform
import argparse
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

OS_TYPE = platform.system()  # Windows or Linux

def banner():
    print(Fore.CYAN + "=" * 55)
    print(Fore.GREEN + "  RIVI Network Diagnostics Toolkit v1.0")
    print(Fore.CYAN + f"  Platform: {OS_TYPE}")
    print(Fore.CYAN + "=" * 55)

def run_ping(target, count=4):
    """Run ping test and return results."""
    print(Fore.YELLOW + f"\n[*] Ping Test → {target}")
    
    if OS_TYPE == "Windows":
        cmd = ["ping", "-n", str(count), target]
    else:
        cmd = ["ping", "-c", str(count), target]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout
        
        if "TTL=" in output or "ttl=" in output or "bytes from" in output:
            print(Fore.GREEN + f"  [PASS] Ping successful to {target}")
            # Extract avg latency
            if "Average" in output:
                avg_line = [l for l in output.split("\n") if "Average" in l]
                if avg_line:
                    print(Fore.GREEN + f"  Stats: {avg_line[0].strip()}")
            return True, output
        else:
            print(Fore.RED + f"  [FAIL] Ping failed to {target}")
            print(Fore.RED + f"  Possible causes:")
            print(Fore.RED + f"    - Target is offline")
            print(Fore.RED + f"    - Firewall blocking ICMP")
            print(Fore.RED + f"    - Wrong IP address")
            return False, output
    except subprocess.TimeoutExpired:
        print(Fore.RED + f"  [FAIL] Ping timed out after 15 seconds")
        return False, "Timeout"

def run_dns_lookup(target):
    """Run DNS lookup for a hostname or IP."""
    print(Fore.YELLOW + f"\n[*] DNS Lookup → {target}")
    
    try:
        # Forward lookup (hostname to IP)
        ip = socket.gethostbyname(target)
        print(Fore.GREEN + f"  [PASS] Resolved: {target} → {ip}")
        
        # Reverse lookup (IP to hostname)
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(Fore.GREEN + f"  [PASS] Reverse: {ip} → {hostname}")
        except socket.herror:
            print(Fore.YELLOW + f"  [WARN] No reverse DNS record for {ip}")
        
        return True, ip
    except socket.gaierror as e:
        print(Fore.RED + f"  [FAIL] DNS resolution failed: {e}")
        print(Fore.RED + f"  Check: Is the DNS server running? Is hostname correct?")
        return False, None

def check_port(target, port, timeout=3):
    """Check if a TCP port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def run_port_scan(target, ports):
    """Check multiple ports on a target."""
    print(Fore.YELLOW + f"\n[*] Port Check → {target}")
    
    port_names = {
        22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB", 389: "LDAP",
        636: "LDAPS", 993: "IMAPS", 995: "POP3S",
        1433: "MSSQL", 3306: "MySQL", 3389: "RDP",
        5985: "WinRM", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    
    results = {}
    for port in ports:
        is_open = check_port(target, port)
        status = "OPEN" if is_open else "CLOSED"
        color = Fore.GREEN if is_open else Fore.RED
        svc = port_names.get(port, "Unknown")
        print(color + f"  [{status}] Port {port} ({svc})")
        results[port] = is_open
    
    return results

def run_traceroute(target):
    """Run traceroute to target."""
    print(Fore.YELLOW + f"\n[*] Traceroute → {target}")
    
    if OS_TYPE == "Windows":
        cmd = ["tracert", "-h", "15", "-w", "1000", target]
    else:
        cmd = ["traceroute", "-m", "15", "-w", "2", target]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print(Fore.WHITE + result.stdout[:2000])
        return result.stdout
    except subprocess.TimeoutExpired:
        print(Fore.RED + "  Traceroute timed out")
        return ""
    except FileNotFoundError:
        print(Fore.RED + f"  traceroute not found. Install with: sudo apt install traceroute")
        return ""

def get_local_network_info():
    """Get local network interface information."""
    print(Fore.YELLOW + "\n[*] Local Network Information")
    
    if OS_TYPE == "Windows":
        result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
    else:
        result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True)
    
    print(Fore.WHITE + result.stdout[:1500])

def generate_report(target, results):
    """Generate a simple text diagnostic report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnostic_report_{target.replace('.', '_')}_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(f"RIVI Network Diagnostic Report\n")
        f.write(f"=" * 50 + "\n")
        f.write(f"Target: {target}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Platform: {OS_TYPE}\n\n")
        
        f.write("Results Summary:\n")
        for test_name, (passed, details) in results.items():
            status = "PASS" if passed else "FAIL"
            f.write(f"  [{status}] {test_name}\n")
    
    print(Fore.GREEN + f"\n[+] Report saved: {filename}")
    return filename

def main():
    parser = argparse.ArgumentParser(description="RIVI Network Diagnostics Toolkit")
    parser.add_argument("--target", help="Single target IP or hostname")
    parser.add_argument("--targets-file", help="File with list of targets")
    parser.add_argument("--ports", help="Comma-separated ports to check", default="22,80,443,3389,445,135")
    parser.add_argument("--traceroute", action="store_true", help="Run traceroute")
    parser.add_argument("--dns-only", action="store_true", help="DNS tests only")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    banner()
    
    targets = []
    if args.target:
        targets = [args.target]
    elif args.targets_file:
        with open(args.targets_file) as f:
            targets = [line.strip() for line in f if line.strip()]
    else:
        targets = [input(Fore.WHITE + "Enter target IP or hostname: ").strip()]
    
    port_list = [int(p.strip()) for p in args.ports.split(",")]
    
    for target in targets:
        print(Fore.CYAN + f"\n{'='*50}")
        print(Fore.CYAN + f"Diagnosing: {target}")
        print(Fore.CYAN + f"{'='*50}")
        
        results = {}
        
        # DNS Lookup first
        dns_ok, resolved_ip = run_dns_lookup(target)
        results["DNS Lookup"] = (dns_ok, resolved_ip)
        
        if args.dns_only:
            continue
        
        # Use resolved IP for further tests if hostname
        test_target = resolved_ip if resolved_ip else target
        
        # Ping test
        ping_ok, ping_output = run_ping(test_target)
        results["Ping Test"] = (ping_ok, ping_output)
        
        # Port scan
        port_results = run_port_scan(test_target, port_list)
        results["Port Scan"] = (any(port_results.values()), port_results)
        
        # Traceroute (optional)
        if args.traceroute:
            tr_output = run_traceroute(test_target)
            results["Traceroute"] = (bool(tr_output), tr_output)
        
        # Generate report
        generate_report(target, results)
    
    # Show local network info
    if args.verbose:
        get_local_network_info()

if __name__ == "__main__":
    main()
