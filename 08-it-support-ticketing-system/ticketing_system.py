#!/usr/bin/env python3
"""
IT Support Ticketing System — L1 Practical Lab
Author: Rithika U | RIVI Enterprises
"""

import json
import os
import sys
import csv
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

DB_FILE = "tickets_db.json"
LOG_FILE = "logs/audit.log"

PRIORITIES = {
    "P1": {"label": "Critical", "response_hours": 1, "resolve_hours": 4},
    "P2": {"label": "High",     "response_hours": 4, "resolve_hours": 8},
    "P3": {"label": "Medium",   "response_hours": 8, "resolve_hours": 24},
    "P4": {"label": "Low",      "response_hours": 24, "resolve_hours": 72},
}

CATEGORIES = ["Hardware", "Software", "Network", "Account", "Security"]
STATUSES = ["Open", "In Progress", "Escalated", "Resolved", "Closed"]

def init_db():
    """Initialize JSON database and log directory."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"tickets": [], "counter": 0}, f, indent=2)
        print(Fore.GREEN + "Database initialized successfully!")
        print(Fore.GREEN + f"Created: {DB_FILE}")
        print(Fore.GREEN + f"Created: {LOG_FILE}")

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_action(action, ticket_id=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {action} {ticket_id}\n")

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + "  RIVI IT Support Ticketing System v1.0")
    print(Fore.CYAN + "=" * 50)

def main_menu():
    print(Fore.YELLOW + "\n[1] Create New Ticket")
    print(Fore.YELLOW + "[2] View All Tickets")
    print(Fore.YELLOW + "[3] Update Ticket Status")
    print(Fore.YELLOW + "[4] Escalate Ticket")
    print(Fore.YELLOW + "[5] Close Ticket")
    print(Fore.YELLOW + "[6] Dashboard")
    print(Fore.YELLOW + "[7] Export Report to CSV")
    print(Fore.RED    + "[0] Exit")
    return input(Fore.WHITE + "\nSelect option: ").strip()

def create_ticket():
    print(Fore.CYAN + "\n--- CREATE NEW TICKET ---")
    db = load_db()
    db["counter"] += 1
    ticket_id = f"TKT-{db['counter']:04d}"

    title = input("Enter ticket title: ").strip()
    
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    cat_idx = int(input("Select category: ")) - 1
    category = CATEGORIES[cat_idx]

    print("\nPriorities:")
    for key, val in PRIORITIES.items():
        print(f"  [{key}] {val['label']}")
    priority = input("Select priority (P1/P2/P3/P4): ").upper().strip()

    user_email = input("Affected user email: ").strip()
    description = input("Description: ").strip()

    now = datetime.now()
    ticket = {
        "id": ticket_id,
        "title": title,
        "category": category,
        "priority": priority,
        "status": "Open",
        "user": user_email,
        "description": description,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "sla_response_by": (now + timedelta(hours=PRIORITIES[priority]["response_hours"])).isoformat(),
        "sla_resolve_by": (now + timedelta(hours=PRIORITIES[priority]["resolve_hours"])).isoformat(),
        "notes": []
    }

    db["tickets"].append(ticket)
    save_db(db)
    log_action("CREATED", ticket_id)

    print(Fore.GREEN + f"\nTicket created successfully!")
    print(Fore.GREEN + f"Ticket ID: {ticket_id}")
    print(Fore.GREEN + f"Priority: {priority} - {PRIORITIES[priority]['label']}")
    print(Fore.YELLOW + f"SLA Response by: {ticket['sla_response_by'][:16]}")

def view_tickets():
    db = load_db()
    tickets = db["tickets"]
    if not tickets:
        print(Fore.YELLOW + "No tickets found.")
        return
    
    print(Fore.CYAN + f"\n{'ID':<12} {'Title':<35} {'Priority':<10} {'Status':<15} {'Category':<12}")
    print("-" * 85)
    for t in tickets:
        color = Fore.RED if t["priority"] == "P1" else Fore.YELLOW if t["priority"] == "P2" else Fore.WHITE
        print(color + f"{t['id']:<12} {t['title'][:33]:<35} {t['priority']:<10} {t['status']:<15} {t['category']:<12}")

def dashboard():
    db = load_db()
    tickets = db["tickets"]
    total = len(tickets)
    open_t = sum(1 for t in tickets if t["status"] == "Open")
    inprog = sum(1 for t in tickets if t["status"] == "In Progress")
    escalated = sum(1 for t in tickets if t["status"] == "Escalated")
    closed = sum(1 for t in tickets if t["status"] in ["Resolved", "Closed"])
    p1 = sum(1 for t in tickets if t["priority"] == "P1" and t["status"] != "Closed")

    print(Fore.CYAN + "\n========== DASHBOARD ==========")
    print(Fore.WHITE + f"Total Tickets:   {total}")
    print(Fore.GREEN + f"Open:            {open_t}")
    print(Fore.YELLOW + f"In Progress:     {inprog}")
    print(Fore.RED + f"Escalated:       {escalated}")
    print(Fore.CYAN + f"Resolved/Closed: {closed}")
    if p1 > 0:
        print(Fore.RED + f"\nWARNING: {p1} P1 Critical ticket(s) open!")

def escalate_ticket():
    ticket_id = input("Enter Ticket ID to escalate: ").strip().upper()
    db = load_db()
    for ticket in db["tickets"]:
        if ticket["id"] == ticket_id:
            print("\n[1] Escalate to L2")
            print("[2] Escalate to L3")
            print("[3] Escalate to Vendor")
            level = input("Select: ").strip()
            notes = input("Escalation notes: ").strip()
            
            level_map = {"1": "L2", "2": "L3", "3": "Vendor"}
            ticket["status"] = "Escalated"
            ticket["notes"].append({
                "timestamp": datetime.now().isoformat(),
                "note": f"Escalated to {level_map.get(level, 'L2')}: {notes}"
            })
            ticket["updated_at"] = datetime.now().isoformat()
            save_db(db)
            log_action(f"ESCALATED to {level_map.get(level)}", ticket_id)
            print(Fore.GREEN + f"Ticket {ticket_id} escalated to {level_map.get(level, 'L2')} successfully!")
            return
    print(Fore.RED + "Ticket not found.")

def export_csv():
    db = load_db()
    filename = f"tickets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "priority", "status", "category", "user", "created_at"])
        writer.writeheader()
        for t in db["tickets"]:
            writer.writerow({k: t.get(k, "") for k in ["id", "title", "priority", "status", "category", "user", "created_at"]})
    print(Fore.GREEN + f"Exported to {filename}")

def main():
    if "--init" in sys.argv:
        init_db()
        return
    
    init_db()
    banner()
    
    while True:
        choice = main_menu()
        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            ticket_id = input("Enter Ticket ID: ").upper()
            db = load_db()
            for t in db["tickets"]:
                if t["id"] == ticket_id:
                    print("Status options:", ", ".join(STATUSES))
                    t["status"] = input("New status: ").strip()
                    save_db(db)
                    print(Fore.GREEN + "Status updated!")
                    break
        elif choice == "4":
            escalate_ticket()
        elif choice == "5":
            ticket_id = input("Enter Ticket ID to close: ").upper()
            db = load_db()
            for t in db["tickets"]:
                if t["id"] == ticket_id:
                    t["status"] = "Closed"
                    t["updated_at"] = datetime.now().isoformat()
                    save_db(db)
                    log_action("CLOSED", ticket_id)
                    print(Fore.GREEN + f"Ticket {ticket_id} closed.")
                    break
        elif choice == "6":
            dashboard()
        elif choice == "7":
            export_csv()
        elif choice == "0":
            print(Fore.CYAN + "Goodbye!")
            break

if __name__ == "__main__":
    main()
