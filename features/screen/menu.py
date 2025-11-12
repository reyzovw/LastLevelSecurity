from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box

def render_gui(console):
    menu_table = Table(
        show_header=True,
        header_style="bold white",
        box=box.ROUNDED,
        border_style="bright_blue",
        title="[red]MAIN MENU[/red]",
        title_style="bold red"
    )

    menu_table.add_column("#", style="red", width=6, justify="center")
    menu_table.add_column("Action", style="white", width=30)
    menu_table.add_column("Description", style="bright")

    menu_items = [
        ("1", "Encrypt Data Block", "Secure encryption of files and directories"),
        ("2", "Decrypt Data Block", "Restore encrypted data with master password"),
        ("3", "LLS Settings", "Configure system preferences and security"),
        ("4", "Password Manager", "Manage stored passwords securely"),
        ("5", "Hash Bruteforce", "Advanced hash cracking tools"),
        ("6", "Shutdown", "Exit the application safely")
    ]

    for num, action, desc in menu_items:
        menu_table.add_row(num, f"[bold]{action}[/bold]", desc)

    console.print()
    console.print(menu_table)
    console.print()

    instruction_panel = Panel(
        Align.center("[bold white]Select an option (1-6) to continue...[/bold white]"),
        style="bright_black",
        box=box.SQUARE
    )
    console.print(instruction_panel)

