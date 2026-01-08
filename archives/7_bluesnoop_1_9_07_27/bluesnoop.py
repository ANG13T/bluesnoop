import asyncio
import time
import json
import csv
import geocoder # New dependency for location tracking
from datetime import datetime
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live
from uuid import UUID

# Import from your menu module
from menu import display_banner, show_about_screen, print_menu_options, get_snoop_time, show_history_menu

console = Console()

GLOBAL_HISTORY = {}

def get_gps_location():
    """Fetches the current Lat/Lng of the device."""
    try:
        # Uses IP-based geolocation (works on most devices with internet)
        g = geocoder.ip('me')
        if g.latlng:
            return f"{g.latlng[0]}, {g.latlng[1]}"
        return "Unknown"
    except Exception:
        return "Unavailable"

def export_data(session_data):
    """Handles exporting the tracked devices including GPS data."""
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
        # Added 'location' to keys
        keys = ["uuid", "name", "first_seen", "last_seen", "location", "sighting_count"]
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

    try:
        with Live(table, refresh_per_second=1, screen=True) as live:
            while True:
                if duration:
                    elapsed = time.time() - start_time
                    if elapsed >= duration:
                        break
                    title = f"\n🦉 BLUESNOOP | TIMED: {int(duration - elapsed)}s left"
                else:
                    title = "\n🦉 BLUESNOOP | LIMITLESS (Ctrl+C to stop)"

                devices = await BleakScanner.discover(timeout=2.0)
                current_ts = datetime.now().strftime("%H:%M:%S")
                # Fetch location once per scan cycle to minimize API calls
                current_loc = get_gps_location()

                for d in devices:
                    uid = d.address
                    name = str(d.name) if d.name else "Unknown"

                    if uid not in GLOBAL_HISTORY:
                        GLOBAL_HISTORY[uid] = {
                            "name": name,
                            "first_seen": current_ts,
                            "last_seen": current_ts,
                            "location": current_loc, # Store initial discovery location
                            "sighting_count": 1
                        }
                    else:
                        GLOBAL_HISTORY[uid]["last_seen"] = current_ts
                        GLOBAL_HISTORY[uid]["location"] = current_loc # Update to current location
                        GLOBAL_HISTORY[uid]["sighting_count"] += 1

                # UI Update logic
                new_table = Table(title=title, border_style="bright_black")
                new_table.add_column("First Seen", style="cyan")
                new_table.add_column("Identifier", style="magenta")
                new_table.add_column("Name", style="green")
                new_table.add_column("Location (Lat, Lng)", style="yellow") # Added Column
                new_table.add_column("Sightings", justify="center")
                new_table.add_column("Last Seen", style="cyan")

                for uid, info in GLOBAL_HISTORY.items():
                    new_table.add_row(
                        info["first_seen"],
                        uid,
                        info["name"],
                        info["location"],
                        str(info["sighting_count"]),
                        info["last_seen"],
                    )

                live.update(new_table)
                await asyncio.sleep(0.5)

    except (asyncio.CancelledError, KeyboardInterrupt):
        console.print("\n[bold yellow]![/bold yellow] Interrupted. Closing scanner and saving intelligence...")

    console.print(f"\n[bold green]✔[/bold green] Intelligence retained. {len(GLOBAL_HISTORY)} targets in memory.")
    # Trigger export automatically or wait for menu return
    export_data(GLOBAL_HISTORY)
    time.sleep(1)

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
            show_history_menu(GLOBAL_HISTORY)
        elif choice == "4":
            show_about_screen()
        elif choice == "5":
            break

if __name__ == "__main__":
    asyncio.run(main_loop())