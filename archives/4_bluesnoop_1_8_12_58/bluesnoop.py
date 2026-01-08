import asyncio
import time
from bleak import BleakScanner
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Import from your new menu module
from menu import display_banner, show_about_screen, print_menu_options, get_snoop_time

console = Console()

HARD_MANUF_NAMES = {
    "LE_WH-1000XM5": "Sony XM5 Headphones",
    "LE-Bose NC 700": "Bose Noise Canceling 700",
}

def get_hardcoded_manuf_name(name):
    if not name or name == "None":
        return "[dim]Unknown[/dim]"
    return HARD_MANUF_NAMES.get(name, name)

async def run_scanner(duration=None):
    start_time = time.time()
    # We use a placeholder table for the Live display
    table = Table()

    with Live(table, refresh_per_second=1, screen=True) as live:
        while True:
            if duration:
                elapsed = time.time() - start_time
                if elapsed >= duration: break
                title = f"\n📡 Timed Snoop: {int(duration - elapsed)}s remaining"
            else:
                title = "\n📡 Limitless Snoop (Ctrl+C to Stop)"

            devices = await BleakScanner.discover(timeout=2.0)

            new_table = Table(title=title)
            new_table.add_column("ID", style="cyan")
            new_table.add_column("UUID Identifier", style="magenta")
            new_table.add_column("Name", style="green")
            new_table.add_column("Manuf", style="yellow")

            for index, d in enumerate(devices):
                new_table.add_row(
                    str(index), d.address, str(d.name),
                    get_hardcoded_manuf_name(d.name), f"<sRSSI> dBm"
                )

            live.update(new_table)
            await asyncio.sleep(0.5)

    input("\nSnoop Complete. Press Enter to return to menu...")

async def main_loop():
    while True:
        console.clear()
        display_banner()
        print_menu_options()

        choice = console.input("\n[bold cyan]Select an option:[/bold cyan] ")

        if choice == "1":
            # Call the new input function from menu.py
            duration = get_snoop_time()
            await run_scanner(duration=duration)
        elif choice == "2":
            try:
                await run_scanner(duration=None)
            except KeyboardInterrupt:
                pass
        elif choice == "3":
            show_about_screen()
        elif choice == "4":
            console.print("[bold red]Exiting...[/bold red]")
            break

if __name__ == "__main__":
    asyncio.run(main_loop())