# 📸 Screenshot Checklist — Network Troubleshooting Lab

Take these IN ORDER. Save with the EXACT filename shown so they match the README automatically.

| # | Filename | What to capture | VM to use |
|---|---|---|---|
| 1 | `01-ipconfig-all-output.png` | Full terminal output of `ipconfig /all` showing IP, gateway, DNS | Windows 11 |
| 2 | `02-ping-gateway-success.png` | `ping 192.168.100.1` with 4 successful replies visible | Windows 11 |
| 3 | `03-ping-domain-controller.png` | `ping 192.168.100.10` with replies visible | Windows 11 |
| 4 | `04-nslookup-dns-test.png` | `nslookup company.local` output showing resolved IP | Windows 11 |
| 5 | `05-kali-network-verification.png` | Terminal with `ip a` + `ping -c 4 192.168.100.10` results | Kali Linux |
| 6 | `06-tracert-route-path.png` | `tracert google.com` showing all hops | Windows 11 |
| 7 | `07-flushdns-renew-fix-applied.png` | All 4 commands (`flushdns`, `release`, `renew`, `registerdns`) run back to back with output | Windows 11 |

## How to take clean screenshots

1. Maximize the terminal/cmd window before capturing — full width looks professional
2. Use `Win + Shift + S` (Windows) for a clean region screenshot, or the Snipping Tool
3. On Kali, use the built-in Screenshot tool or `gnome-screenshot -a` for area select
4. Crop out anything personal (your real name in the prompt, if visible) before uploading to GitHub
5. Save all 7 into the `screenshots/` folder using the exact filenames above — GitHub will render them automatically since the README already links to them

## Tip for LinkedIn

Pick 2–3 of the cleanest screenshots (gateway ping success + DNS resolution + the fix being applied) and post them as a carousel with a short caption like:

> "Diagnosed and resolved a simulated DNS/DHCP outage across a 3-tier VM lab (Windows Server 2019, Windows 11, Kali Linux) using a layer-by-layer troubleshooting approach. Full writeup on GitHub 👇"
