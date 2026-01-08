import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

def display_banner():
    """Reads the banner from banner.txt and displays it."""
    banner_path = "banner.txt"
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            banner_content = f.read()
    except FileNotFoundError:
        banner_content = "BLUETOOTH SNOOPER\n[File banner.txt not found]"

    banner_text = Text(banner_content, style="bold cyan")
    console.print(Align.center(Panel(banner_text, subtitle="Bluetooth SIGINT Utility - v0.0.1", subtitle_align="right")))

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