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
    session_data = {} # {uuid: {name, manufs, first_seen, last_seen}}
    table = Table()

    try:
        with Live(table, refresh_per_second=1, screen=True) as live:
            while True:
                if duration:
                    elapsed = time.time() - start_time
                    if elapsed >= duration: break
                    title = f"📡 Timed Snoop: {int(duration - elapsed)}s remaining"
                else:
                    title = "📡 Limitless Snoop (Ctrl+C to Stop & Export)"

                devices = await BleakScanner.discover(timeout=2.0)
                current_ts = datetime.now().strftime("%H:%M:%S")

                for d in devices:
                    uuid = d.address
                    name = str(d.name) if d.name else "Unknown"

                    if uuid not in session_data:
                        session_data[uuid] = {
                            "name": name,
                            "manuf": get_hardcoded_manuf_name(name),
                            "first_seen": current_ts,
                            "last_seen": current_ts
                        }
                    else:
                        # Update existing entry
                        session_data[uuid]["last_seen"] = current_ts

                # UI Update
                new_table = Table(title=title)
                new_table.add_column("First Seen", style="dim")
                new_table.add_column("UUID Identifier", style="magenta")
                new_table.add_column("Name", style="green")
                new_table.add_column("Last Seen", style="dim")

                for uuid, data in session_data.items():
                    new_table.add_row(
                        data["first_seen"], uuid, data["name"], data["last_seen"]
                    )

                live.update(new_table)
                await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        pass # Allow clean exit to export for Limitless mode

    export_data(session_data)
    input("\nPress Enter to return to menu...")

async def main_loop():
    while True:
        console.clear()
        display_banner()
        print_menu_options()

        choice = console.input("\n[bold cyan]Select an option:[/bold cyan] ")

        if choice == "1":
            duration = get_snoop_time()
            await run_scanner(duration=duration)
        elif choice == "2":
            await run_scanner(duration=None)
        elif choice == "3":
            show_about_screen()
        elif choice == "4":
            console.print("[bold red]Exiting SIGINT Utility...[/bold red]")
            break

if __name__ == "__main__":
    asyncio.run(main_loop())