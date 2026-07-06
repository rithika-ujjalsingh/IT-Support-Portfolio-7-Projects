# 📸 Screenshot Checklist — DNS & DHCP Infrastructure

| # | Filename | What to capture | VM to use |
|---|---|---|---|
| 1 | `01-dns-a-record-created.png` | DNS Manager showing the new "webserver" A record in the zone list | Windows Server 2019 |
| 2 | `02-nslookup-resolution-success.png` | cmd output of `nslookup webserver.company.local` showing the resolved IP | Windows 11 |
| 3 | `03-cname-alias-created.png` | DNS Manager showing the "www" alias record pointing to webserver | Windows Server 2019 |
| 4 | `04-reverse-lookup-zone-created.png` | DNS Manager Reverse Lookup Zones list showing the new 192.168.100.x zone | Windows Server 2019 |
| 5 | `05-kali-dig-dns-verification.png` | Kali terminal output of the `dig` command | Kali Linux |
| 6 | `06-dhcp-scope-configuration.png` | DHCP Manager scope properties showing the range and exclusions | Windows Server 2019 |
| 7 | `07-dhcp-reservation-created.png` | DHCP Manager Reservations folder showing the new reservation entry | Windows Server 2019 |
| 8 | `08-dhcp-renewal-confirmation.png` | cmd output of `ipconfig /all` after renewal, showing the IP within scope range | Windows 11 |
