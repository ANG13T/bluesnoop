import asyncio
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

HARD_MANUF_NAMES = {
    "LE_WH-1000XM5": "Sony XM5 Headphones",
    "LE-Bose NC 700": "Bose Noise Canceling 700",
    "MI Band 6": "Xiaomi Fitness Tracker"
}

def get_hardcoded_manuf_name(name):
    if not name or name == "None":
        return "[dim]Unknown Device[/dim]"
    return HARD_MANUF_NAMES.get(name, "Unknown Device")

async def scan_to_table():
    # Create the table structure
    table = Table(title="📡 Bluetooth Signal Intelligence", highlight=True)
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Identifier (UUID)", style="magenta")
    table.add_column("Name", style="green")
    table.add_column("Status", justify="center")

    # Use Live to update the table in real-time
    with Live(table, refresh_per_second=1) as live:
        while True:
            devices = await BleakScanner.discover(timeout=2.0)

            # Clear and rebuild the table for the new scan results
            new_table = Table(title="📡 Bluetooth Signal Intelligence")
            new_table.add_column("Idx", style="cyan")
            new_table.add_column("Identifier (UUID)", style="magenta")
            new_table.add_column("Name", style="green")
            new_table.add_column("Manuf", style="yellow")

            for index, d in enumerate(devices):
                name = d.name if d.name else "[dim]Unknown[/dim]"

                new_table.add_row(
                    str(index),
                    d.address,
                    name,
                    get_hardcoded_manuf_name(name)
                )

            live.update(new_table)
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(scan_to_table())
    except KeyboardInterrupt:
        console.print("\n[bold red]Stopping Scanner...[/bold red]")