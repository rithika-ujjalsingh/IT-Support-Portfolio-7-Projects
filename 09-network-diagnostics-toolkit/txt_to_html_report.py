import sys
import os
from datetime import datetime

def convert(txt_path):
    if not os.path.exists(txt_path):
        print(f"[!] File not found: {txt_path}")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    html_path = os.path.splitext(txt_path)[0] + ".html"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>RIVI Network Diagnostics Report</title>
<style>
    body {{ background: #0d1117; color: #c9d1d9; font-family: 'Consolas', 'Courier New', monospace; padding: 40px; line-height: 1.6; }}
    .container {{ max-width: 900px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 30px; }}
    h1 {{ color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 12px; }}
    .meta {{ color: #8b949e; font-size: 13px; margin-bottom: 20px; }}
    pre {{ white-space: pre-wrap; word-wrap: break-word; background: #0d1117; padding: 20px; border-radius: 6px; border: 1px solid #21262d; }}
    footer {{ margin-top: 20px; color: #6e7681; font-size: 12px; text-align: right; }}
</style>
</head>
<body>
    <div class="container">
        <h1>Network Diagnostics Report</h1>
        <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Source: {os.path.basename(txt_path)}</div>
        <pre>{content}</pre>
        <footer>RIVI Enterprises - Network Diagnostics Toolkit v1.0</footer>
    </div>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] HTML report saved: {html_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python txt_to_html_report.py <report.txt>")
        sys.exit(1)
    convert(sys.argv[1])