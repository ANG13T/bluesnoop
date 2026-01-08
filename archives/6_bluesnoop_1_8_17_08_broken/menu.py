import os
import json
import csv
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table

console = Console()

# --- HISTORY & EXPORT LOGIC ---

def display_history_table(data):
    table = Table(title="Captured Device History")
    table.add_column("Identifier", style="magenta")
    table.add_column("Name", style="green")
    table.add_column("First Seen", style="dim")
    table.add_column("Last Seen", style="dim")

    for uid, info in data.items():
        table.add_row(
            uid,
            str(info['name']),
            info['first_seen'],
            info['last_seen']
        )

    console.print(table)
    input("\nPress Enter to return to History Menu...")

def export_intel(data, format_type):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"BLUESNOOP_DUMP_{ts}.{format_type}"

    if format_type == "json":
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    else:
        # CSV Export Logic
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["UUID", "Name", "First Seen", "Last Seen"])
            for uid, info in data.items():
                writer.writerow([uid, info['name'], info['first_seen'], info['last_seen']])

    console.print(f"[bold green]✔[/bold green] Success: Intel exported to {filename}")
    time.sleep(2)

def show_history_menu(history_data):
    if not history_data:
        console.print("[yellow]No intelligence gathered yet. Start a snoop first.[/yellow]")
        input("\nPress Enter...")
        return

    while True:
        console.clear()
        display_banner()
        console.print("[bold cyan]DATABASE: SIGHTED TARGETS[/bold cyan]\n")

        # Choice menu for History
        console.print("[bold]1.[/bold] View All Sighted Devices")
        console.print("[bold]2.[/bold] Export to JSON")
        console.print("[bold]3.[/bold] Export to CSV")
        console.print("[bold]4.[/bold] Return to Main Menu")

        sub_choice = console.input("\n[bold cyan]Intel Action > [/bold cyan]")

        if sub_choice == "1":
            display_history_table(history_data)
        elif sub_choice == "2":
            export_intel(history_data, "json")
        elif sub_choice == "3":
            export_intel(history_data, "csv")
        elif sub_choice == "4":
            break

# --- CORE UI ELEMENTS ---

def display_banner():
    """Reads the banner from banner.txt and displays it."""
    banner_path = "banner.txt"
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            banner_content = f.read()
    except FileNotFoundError:
        banner_content = "BLUESNOOP\n[File banner.txt not found]"

    banner_text = Text(banner_content, style="bold cyan")
    console.print(banner_text)

def get_snoop_time():
    """Prompts user for duration with default and max constraints."""
    console.print("\n[bold yellow]Timed Snoop Configuration[/bold yellow]")
    console.print("Default: [cyan]30s[/cyan] | Max: [cyan]300s (5mins)[/cyan]")

    user_input = console.input("Enter duration in seconds (or press Enter for default): ").strip()

    if not user_input:
        return 30

    try:
        seconds = int(user_input)
        if seconds > 300:
            console.print("[bold red]![/bold red] Max limit exceeded. Setting to 300s.")
            return 300
        if seconds <= 0:
            return 30
        return seconds
    except ValueError:
        return 30

def show_about_screen():
    about_text = """
    [bold cyan]BLUESNOOP v1.0[/bold cyan]
    
    A lightweight Bluetooth Signal Intelligence (SIGINT) utility.
    
    [bold yellow]Capabilities:[/bold yellow]
    - [bold]Passive Recon:[/bold] Identify nearby device UUIDs and Names.
    - [bold]Session Memory:[/bold] Persistent tracking of first/last appearance.
    - [bold]Friendly Mapping:[/bold] Translation of cryptic model IDs.
    - [bold]Data Dumping:[/bold] Export intelligence for external analysis.
    """
    console.print(Panel(about_text, title="Intel Briefing", border_style="bright_black"))
    input("\nPress Enter to return to menu...")

def print_menu_options():
    console.print("[bold]1.[/bold]  ⏱️  Timed Snoop")
    console.print("[bold]2.[/bold]  ♾️  Limitless Snoop")
    console.print("[bold]3.[/bold]  🗂️  View/Export History")
    console.print("[bold]4.[/bold]  ℹ️  About")
    console.print("[bold]5.[/bold]  ❌ Quit")