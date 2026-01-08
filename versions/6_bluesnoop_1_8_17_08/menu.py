import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

def display_history_table(data):
    table = Table(title="Captured Device History")
    table.add_column("Identifier", style="magenta")
    table.add_column("Name", style="green")
    table.add_column("First Seen", style="dim")
    table.add_column("Last Seen", style="dim")
    table.add_column("Peak RSSI", justify="right")

    for uid, info in data.items():
        table.add_row(
            uid,
            str(info['name']),
            info['first_seen'],
            info['last_seen'],
            f"{info['max_rssi']} dBm"
        )

    console.print(table)
    input("\nPress Enter to return to History Menu...")

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
            writer.writerow(["UUID", "Name", "First Seen", "Last Seen", "Max RSSI"])
            for uid, info in data.items():
                writer.writerow([uid, info['name'], info['first_seen'], info['last_seen'], info['max_rssi']])

    console.print(f"[bold green]✔[/bold green] Success: Intel exported to {filename}")
    time.sleep(2)

def display_banner():
    """Reads the banner from banner.txt and displays it."""
    banner_path = "banner.txt"
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            banner_content = f.read()
    except FileNotFoundError:
        banner_content = "BLUETOOTH SNOOPER\n[File banner.txt not found]"

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
            console.print("[bold red]![/bold red] Invalid time. Setting to 30s.")
            return 30
        return seconds
    except ValueError:
        console.print("[bold red]![/bold red] Non-numeric input. Using default 30s.")
        return 30

def show_about_screen():
    about_text = """
    [bold cyan]Bluetooth Snooper v1.0[/bold cyan]
    
    This utility is designed for lightweight signal intelligence.
    It maps nearby BLE devices using their UUID and broadcast names.
    
    [bold yellow]Modes:[/bold yellow]
    - [bold]Timed Snoop:[/bold] Snapshot reconnaissance with custom duration.
    - [bold]Limitless:[/bold] Continuous tracking until manually stopped.
    """
    console.print(Panel(about_text, title="About"))
    input("\nPress Enter to return to menu...")

def print_menu_options():
    console.print("[bold]1.[/bold]  Timed Snoop")
    console.print("[bold]2.[/bold]  Limitless Snoop")
    console.print("[bold]3.[/bold]  About")
    console.print("[bold]4.[/bold]  Quit")