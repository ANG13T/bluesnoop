import asyncio
import time
import json
import csv
from datetime import datetime
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Import from your menu module
from menu import display_banner, show_about_screen, print_menu_options, get_snoop_time

console = Console()

GLOBAL_HISTORY = {}

HARD_MANUF_NAMES = {
    "LE_WH-1000XM5": "Sony XM5 Headphones",
    "LE-Bose NC 700": "Bose Noise Canceling 700",
}

def get_hardcoded_manuf_name(name):
    if not name or name == "None":
        return "Unknown"
    return HARD_MANUF_NAMES.get(name, "Generic/Other")

def export_data(session_data):
    """Handles exporting the tracked devices to various formats."""
    if not session_data:
        console.print("[yellow]No data to export.[/yellow]")
        return

    console.print("\n[bold cyan]Export Results[/bold cyan]")
    console.print("1. JSON | 2. CSV | 3. Skip")
    choice = console.input("Select format: ").strip()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        filename = f"snoop_report_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)
        console.print(f"[green]Saved to {filename}[/green]")
    elif choice == "2":
        filename = f"snoop_report_{timestamp}.csv"
        keys = ["uuid", "name", "manuf", "first_seen", "last_seen"]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for uuid, data in session_data.items():
                row = {"uuid": uuid, **data}
                writer.writerow(row)
        console.print(f"[green]Saved to {filename}[/green]")
    else:
        console.print("[yellow]Export skipped.[/yellow]")

async def run_scanner(duration=None):
    start_time = time.time()
    table = Table()

    with Live(table, refresh_per_second=1, screen=True) as live:
        while True:
            # 1. Timing Logic
            if duration:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
                title = f"\n🦉 BLUESNOOP | TIMED: {int(duration - elapsed)}s left"
            else:
                title = "\n🦉 BLUESNOOP | LIMITLESS (Ctrl+C to stop)"

            # 2. Perform the Scan
            # Discover finds all devices currently broadcasting
            devices = await BleakScanner.discover(timeout=2.0)
            current_ts = datetime.now().strftime("%H:%M:%S")

            # 3. Intelligence Update (No RSSI)
            for d in devices:
                uid = d.address
                name = str(d.name) if d.name else "Unknown"

                if uid not in GLOBAL_HISTORY:
                    # Target's first appearance
                    GLOBAL_HISTORY[uid] = {
                        "name": name,
                        "manuf": get_hardcoded_manuf_name(name),
                        "first_seen": current_ts,
                        "last_seen": current_ts,
                        "sighting_count": 1
                    }
                else:
                    # Target is still present - update last seen and count
                    GLOBAL_HISTORY[uid]["last_seen"] = current_ts
                    GLOBAL_HISTORY[uid]["sighting_count"] += 1

            # 4. Interface Refresh
            new_table = Table(title=title, border_style="bright_black")
            new_table.add_column("First Seen", style="cyan", no_wrap=True)
            new_table.add_column("Identifier (UUID)", style="magenta")
            new_table.add_column("Name / Friendly", style="green")
            new_table.add_column("Sightings", justify="center", style="yellow")
            new_table.add_column("Last Seen", style="cyan", no_wrap=True)

            for uid, info in GLOBAL_HISTORY.items():
                new_table.add_row(
                    info["first_seen"],
                    uid,
                    f"{info['name']} ({info['manuf']})",
                    str(info["sighting_count"]),
                    info["last_seen"]
                )

            live.update(new_table)
            await asyncio.sleep(0.5)

    console.print(f"\n[bold green]✔[/bold green] Intelligence collection complete.")
    input("Press Enter to return to menu...")

async def main_loop():
    while True:
        console.clear()
        display_banner()
        print_menu_options()

        choice = console.input("\n[bold cyan]Select Option > [/bold cyan]")

        if choice == "1":
            t = get_snoop_time()
            await run_scanner(duration=t)
        elif choice == "2":
            await run_scanner(duration=None)
        elif choice == "3":
            # Pass the global history to the new menu in menu.py
            show_history_menu(GLOBAL_HISTORY)
        elif choice == "4":
            show_about_screen()
        elif choice == "5":
            break

if __name__ == "__main__":
    asyncio.run(main_loop())