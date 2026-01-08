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

def show_about_screen():
    about_text = """
    [bold cyan]Bluetooth Snooper v1.0[/bold cyan]
    
    This utility is designed for lightweight signal intelligence.
    It maps nearby BLE devices using their UUID and broadcast names.
    
    [bold yellow]Modes:[/bold yellow]
    - [bold]Timed Snoop:[/bold] Runs a 30s scan for a quick snapshot of the area.
    - [bold]Limitless:[/bold] Continuous reconnaissance until interrupted.
    """
    console.print(Panel(about_text, title="About"))
    input("\nPress Enter to return to menu...")

def print_menu_options():
    console.print("[bold]1.[/bold]  Timed Snoop")
    console.print("[bold]2.[/bold]  Limitless Snoop")
    console.print("[bold]3.[/bold]  About")
    console.print("[bold]4.[/bold]  Quit")