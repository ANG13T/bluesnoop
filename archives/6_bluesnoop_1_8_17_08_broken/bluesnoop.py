import asyncio
import time
import json
import csv
from datetime import datetime
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live
from bluetooth_numbers import service, exceptions
from uuid import UUID

# Import from your menu module
from menu import display_banner, show_about_screen, print_menu_options, get_snoop_time, show_history_menu

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

    # Wrap the entire scanner in a try block
    try:
        with Live(table, refresh_per_second=1, screen=True) as live:
            while True:
                if duration:
                    elapsed = time.time() - start_time
                    if elapsed >= duration:
                        break
                    title = f"🦉 BLUESNOOP | TIMED: {int(duration - elapsed)}s left"
                else:
                    title = "🦉 BLUESNOOP | LIMITLESS (Ctrl+C to stop)"

                # The crash usually happens right here during the 'await'
                devices = await BleakScanner.discover(timeout=2.0)
                current_ts = datetime.now().strftime("%H:%M:%S")

                for d in devices:
                    uid = d.address

                    name = str(d.name) if d.name else "Unknown"

                    try:
                        manufacturer = service[UUID(name)]
                    except KeyError:
                        manufacturer = "Unknown"
                    except exceptions.InvalidUUIDError:
                        manufacturer = "Unknown"

                    if uid not in GLOBAL_HISTORY:
                        GLOBAL_HISTORY[uid] = {
                            "name": name,
                            "manuf": manufacturer,
                            "first_seen": current_ts,
                            "last_seen": current_ts,
                            "sighting_count": 1
                        }
                    else:
                        GLOBAL_HISTORY[uid]["last_seen"] = current_ts
                        GLOBAL_HISTORY[uid]["sighting_count"] += 1

                # UI Update logic
                new_table = Table(title=title, border_style="bright_black")
                new_table.add_column("First Seen", style="cyan")
                new_table.add_column("Identifier", style="magenta")
                new_table.add_column("Name", style="green")
                new_table.add_column("Sightings", justify="center")
                new_table.add_column("Last Seen", style="cyan")
                new_table.add_column("Target Manuf", style="yellow")

                try:
                    manufacturer = service[UUID(name)]
                except KeyError:
                    manufacturer = "Unknown"
                except exceptions.InvalidUUIDError:
                    manufacturer = "Unknown"

                for uid, info in GLOBAL_HISTORY.items():
                    new_table.add_row(
                        info["first_seen"], uid, info["name"],
                        str(info["sighting_count"]), info["last_seen"],
                        manufacturer
                    )

                live.update(new_table)
                await asyncio.sleep(0.5)

    except (asyncio.CancelledError, KeyboardInterrupt):
        # This catch is what prevents the crash and allows the data to stay in memory
        console.print("\n[bold yellow]![/bold yellow] Interrupted. Closing scanner and saving intelligence...")

    # This code will now actually run after Ctrl+C
    console.print(f"\n[bold green]✔[/bold green] Intelligence retained. {len(GLOBAL_HISTORY)} targets in memory.")
    time.sleep(1) # Brief pause so the user sees the message

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