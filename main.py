from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box
from rich.align import Align
import time

from features.encryption.methods import generate_static_code
from features.utils.console import cls
from features.encryption.bruteforce import Bruteforce
from features.screen.menu import render_gui
from features.utils.models import PasswordModel
from features.utils.file import *
from init import *

console = Console()

def print_header():
    header_text = Text("LAST LEVEL SECURITY", style="bold white")
    header = Panel(
        Align.center(header_text),
        style="red",
        box=box.HEAVY_EDGE
    )
    console.print(header)

def print_footer():
    """Красивый футер"""
    footer_text = Text(f"Version: {VERSION} {RELEASE} | Author: @{AUTHOR}", style="dim white")
    footer = Panel(
        Align.center(footer_text),
        style="red",
        box=box.ROUNDED
    )
    console.print(footer)

def show_loading(message="Processing..."):
    """Красивый индикатор загрузки"""
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)
        time.sleep(1)

def show_progress_bar(total=100, description="Processing"):
    """Прогресс-бар для длительных операций"""
    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
    ) as progress:
        task = progress.add_task(description, total=total)
        for i in range(total):
            progress.update(task, advance=1)
            time.sleep(0.02)

def draw_bruteforce_menu():
    cls()
    print_header()

    console.print(Panel(
        "🔍 [bold yellow]Hash Bruteforce Tool[/bold yellow]\n\n"
        "Press [bold red]Ctrl + C[/bold red] to go back",
        style="yellow"
    ))

    # Таблица с типами хэшей
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("№", style="cyan", width=5)
    table.add_column("Hash Type", style="green")
    table.add_column("Description", style="white")

    hash_types = [
        ("1", "SHA-256", "256-bit secure hash algorithm"),
        ("2", "MD-5", "128-bit message digest (less secure)"),
        ("3", "SHA-224", "224-bit secure hash algorithm"),
        ("4", "SHA-512", "512-bit secure hash algorithm"),
        ("5", "SHA-1", "160-bit secure hash algorithm (deprecated)")
    ]

    for num, htype, desc in hash_types:
        table.add_row(num, htype, desc)

    console.print(table)
    console.print()

    hash_type = int(Prompt.ask("🎯 [bold cyan]Hash type[/bold cyan]"))
    target_hash = Prompt.ask("🔑 [bold cyan]Hash value[/bold cyan]")

    bruteforce = Bruteforce(hash_type, target_hash)

    # Прогресс бар для брутфорса
    console.print()
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
    ) as progress:
        task = progress.add_task("[red]Bruteforcing hash...", total=100)

        # Симуляция прогресса (замените на реальный прогресс из bruteforce.run())
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.05)

    result = bruteforce.run()

    cls()
    print_header()

    if result['found']:
        success_panel = Panel(
            f"✅ [bold green]SUCCESS![/bold green]\n\n"
            f"🔓 [bold white]Decrypted value:[/bold white] [green]{result['word']}[/green]\n"
            f"📄 [bold white]Original hash:[/bold white] [cyan]{result['hash']}[/cyan]",
            title="🎉 Bruteforce Complete",
            style="green",
            box=box.DOUBLE_EDGE
        )
        console.print(success_panel)
    else:
        error_panel = Panel(
            "❌ [bold red]Hash not found[/bold red]\n\n"
            "The target hash could not be decrypted with available methods",
            title="😞 Bruteforce Failed",
            style="red",
            box=box.ROUNDED
        )
        console.print(error_panel)

    console.print()
    Prompt.ask("🔄 Press [bold green]Enter[/bold green] to go back")

def draw_main_menu():
    cls()
    print_header()

    # Информационная панель
    info_panel = Panel(
        f"[bold white]Version:[/bold white] [italic white]{VERSION} {RELEASE}[/italic white]\n"
        f"[bold white]Author:[/bold white] [italic white]@{AUTHOR}[/italic white]",
        style="red",
        box=box.ROUNDED
    )
    console.print(info_panel)

    console.print()  # Отступ

    # Основное меню
    render_gui(console)  # Ваша существующая функция

    console.print()  # Отступ

    return int(Prompt.ask("[bold white]Action number[/bold white]"))

def add_password_callback(password_head: str, master_password: str):
    cls()
    print_header()

    console.print(Panel(
        "➕ [bold green]Add New Password[/bold green]\n\n"
        "Press [bold red]Ctrl + C[/bold red] to go back",
        style="green"
    ))

    password_value = Prompt.ask("🔑 [bold cyan]Password value[/bold cyan]", password=True)

    cls()
    print_header()

    if Confirm.ask("❓ [bold yellow]Do you really want to create this password?[/bold yellow]"):
        show_loading("Creating password...")

        passwords.add_password(password_head, password_value, master_password)

        success_panel = Panel(
            "✅ [bold green]Password created successfully![/bold green]",
            style="green",
            box=box.DOUBLE_EDGE
        )
        console.print(success_panel)
        time.sleep(1)
        open_password_manager(master_password)
    else:
        raise KeyboardInterrupt

def open_password_data(cipher: AESCipher, password_id: int, msp: str):
    try:
        cls()
        print_header()

        console.print(Panel(
            "📋 [bold cyan]Password Details[/bold cyan]\n\n"
            "Press [bold red]Ctrl + C[/bold red] to go back",
            style="cyan"
        ))

        # Таблица действий
        actions_table = Table(show_header=False, box=box.SIMPLE)
        actions_table.add_column("Action", style="white")
        actions_table.add_row("1 - 🗑️ Remove Password")
        console.print(actions_table)

        console.print()  # Отступ

        data = passwords.get_password(password_id)

        if data:
            decrypted_data = PasswordModel(
                id=data.id,
                name=cipher.decrypt(data.name),
                value=cipher.decrypt(data.value)
            )

            # Панель с данными пароля
            password_panel = Panel(
                f"🆔 [bold white]ID:[/bold white] [yellow]{decrypted_data.id}[/yellow]\n"
                f"📝 [bold white]Head:[/bold white] [cyan]{decrypted_data.name}[/cyan]\n"
                f"🔒 [bold white]Data:[/bold white] [green]{'*' * len(decrypted_data.value)}[/green]",
                title="🔐 Password Information",
                style="bright_blue",
                box=box.ROUNDED
            )
            console.print(password_panel)

            action_number = int(Prompt.ask("\n🎯 [bold cyan]Action number[/bold cyan]"))

            match action_number:
                case 1:
                    cls()
                    print_header()

                    if Confirm.ask("⚠️ [bold red]Do you really want to delete this password?[/bold red]"):
                        show_loading("Deleting password...")
                        passwords.remove_password(password_id)

                        success_panel = Panel(
                            f"✅ [bold green]Password #{password_id} was successfully removed[/bold green]",
                            style="green"
                        )
                        console.print(success_panel)
                        raise KeyboardInterrupt
                    else:
                        info_panel = Panel(
                            "ℹ️ [bold yellow]Deletion cancelled[/bold yellow]",
                            style="yellow"
                        )
                        console.print(info_panel)
        else:
            error_panel = Panel(
                "❌ [bold red]No such password exists[/bold red]",
                style="red"
            )
            console.print(error_panel)
            time.sleep(1.5)
            raise KeyboardInterrupt

    except KeyboardInterrupt:
        open_password_manager(msp)

def open_password_manager(master_password: str):
    cls()
    print_header()

    console.print(Panel(
        "🔐 [bold cyan]Password Manager[/bold cyan]\n\n"
        "Press [bold red]Ctrl + C[/bold red] to go back\n"
        "💡 [bold white]a[/bold white] - Add password\n"
        "💡 [bold white]Enter ID[/bold white] - Edit password",
        style="cyan"
    ))

    all_passwords = passwords.get_all_name_and_id()
    aes = AESCipher(master_password)

    # Таблица паролей
    if all_passwords:
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")

        for data in all_passwords:
            name_of_part = aes.decrypt(data.name)
            table.add_row(str(data.id), name_of_part, "✅ Active")

        console.print(table)
    else:
        console.print(Panel(
            "📭 [bold yellow]No passwords stored yet[/bold yellow]",
            style="yellow"
        ))

    console.print()  # Отступ
    edit_id = Prompt.ask("🎮 [bold cyan]Action or password ID[/bold cyan]")

    if str(edit_id).isnumeric():
        if int(edit_id) in [data.id for data in all_passwords]:
            open_password_data(aes, edit_id, master_password)
        else:
            error_panel = Panel(
                "❌ [bold red]No password found for this ID[/bold red]",
                style="red"
            )
            console.print(error_panel)
            time.sleep(1.5)
            open_password_manager(master_password)
    elif edit_id == "a":
        cls()
        print_header()

        console.print(Panel(
            "➕ [bold green]Add New Password[/bold green]\n\n"
            "Press [bold red]Ctrl + C[/bold red] to go back",
            style="green"
        ))

        password_head = Prompt.ask("📝 [bold cyan]Password head[/bold cyan]")
        add_password_callback(password_head, master_password)

def enter_to_password_manager():
    cls()
    print_header()

    console.print(Panel(
        "🔐 [bold cyan]Master Authentication[/bold cyan]\n\n"
        "Press [bold red]Ctrl + C[/bold red] to go back",
        style="cyan"
    ))

    master_password = generate_static_code(Prompt.ask("🔑 [bold cyan]Enter your master password[/bold cyan]", password=True))

    try:
        open_password_manager(master_password)
    except ValueError:
        error_panel = Panel(
            "❌ [bold red]Master password is incorrect[/bold red]",
            style="red"
        )
        console.print(error_panel)

def open_settings(user_config_data: dict):
    cls()
    print_header()

    console.print(Panel(
        "⚙️ [bold yellow]System Settings[/bold yellow]\n\n"
        "Press [bold red]Ctrl + C[/bold red] to go back",
        style="yellow"
    ))

    # Таблица настроек
    table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
    table.add_column("№", style="cyan", width=5)
    table.add_column("Setting", style="white")
    table.add_column("Status", style="yellow")
    table.add_column("Description", style="dim white")

    settings = [
        ("1", "Use initialization vector",
         "✅ ENABLED" if user_config_data['use_iv'][0] else "❌ DISABLED",
         user_config_data['use_iv'][2]),
        ("2", "Use HMAC",
         "✅ ENABLED" if user_config_data['use_hmac'][0] else "❌ DISABLED",
         user_config_data['use_hmac'][2]),
        ("3", "Compress blocks",
         "✅ ENABLED" if user_config_data['compress_blocks'][0] else "❌ DISABLED",
         user_config_data['compress_blocks'][2])
    ]

    for num, setting, status, desc in settings:
        table.add_row(num, setting, status, desc)

    console.print(table)
    console.print()

    edit_id = int(Prompt.ask("🎯 [bold cyan]Action number[/bold cyan]"))

    match edit_id:
        case 1:
            new_value = not user_config_data['use_iv'][0]
            json_parser.edit_data("use_iv", [new_value, True, "Will be no randomization, 'Strong impact'"])
            status = "enabled" if new_value else "disabled"
            show_loading(f"{'Enabling' if new_value else 'Disabling'} IV...")
        case 2:
            new_value = not user_config_data['use_hmac'][0]
            json_parser.edit_data("use_hmac", [new_value, True, "Increase the file size, 'Improved security'"])
            status = "enabled" if new_value else "disabled"
            show_loading(f"{'Enabling' if new_value else 'Disabling'} HMAC...")
        case 3:
            new_value = not user_config_data['compress_blocks'][0]
            json_parser.edit_data("compress_blocks", [new_value, True, "Reducing block size"])
            status = "enabled" if new_value else "disabled"
            show_loading(f"{'Enabling' if new_value else 'Disabling'} compression...")

    success_panel = Panel(
        f"✅ [bold green]Setting {status} successfully![/bold green]",
        style="green"
    )
    console.print(success_panel)
    time.sleep(1)

    new_user_data = json_parser.get_user_config_data()
    open_settings(new_user_data)

def main():
    os.system(f"title LLS / build #{VERSION} {RELEASE}")
    cls()

    while True:
        user_config_data = json_parser.get_user_config_data()

        try:
            action_number = draw_main_menu()

            match action_number:
                case 1:
                    try:
                        cls()
                        print_header()

                        console.print(Panel(
                            "🔒 [bold green]Data Encryption[/bold green]\n\n"
                            "Press [bold red]Ctrl + C[/bold red] to go back",
                            style="green"
                        ))

                        directory = Prompt.ask("📁 [bold cyan]Data directory[/bold cyan]")
                        block_name = Prompt.ask("📝 [bold cyan]Block name[/bold cyan]")
                        master_password = generate_static_code(Prompt.ask("🔑 [bold cyan]Master password[/bold cyan]", password=True))

                        console.print()
                        show_progress_bar(description="[cyan]Encrypting data...")

                        run_encryption(directory + "/", block_name, master_password,
                                       hmac=user_config_data['use_hmac'][0], iv=user_config_data['use_iv'][0])

                        success_panel = Panel(
                            "✅ [bold green]The block was successfully encrypted![/bold green]",
                            style="green",
                            box=box.DOUBLE_EDGE
                        )
                        console.print(success_panel)

                    except KeyboardInterrupt:
                        cls()
                        continue
                case 2:
                    try:
                        cls()
                        print_header()

                        console.print(Panel(
                            "🔓 [bold blue]Data Decryption[/bold blue]\n\n"
                            "Press [bold red]Ctrl + C[/bold red] to go back",
                            style="blue"
                        ))

                        directory = Prompt.ask("📁 [bold cyan]Block directory[/bold cyan]")
                        master_password = generate_static_code(Prompt.ask("🔑 [bold cyan]Master password[/bold cyan]", password=True))

                        console.print()
                        show_progress_bar(description="[blue]Decrypting data...")

                        run_decryption(directory + "/", master_password, hmac=user_config_data['use_hmac'][0],
                                       iv=user_config_data['use_iv'][0])

                        success_panel = Panel(
                            "✅ [bold green]The block was successfully decrypted![/bold green]",
                            style="green",
                            box=box.DOUBLE_EDGE
                        )
                        console.print(success_panel)

                    except KeyboardInterrupt:
                        cls()
                        continue
                case 3:
                    try:
                        open_settings(user_config_data)
                    except KeyboardInterrupt:
                        cls()
                        continue
                case 4:
                    try:
                        enter_to_password_manager()
                    except KeyboardInterrupt:
                        cls()
                        continue
                case 5:
                    try:
                        draw_bruteforce_menu()
                    except KeyboardInterrupt:
                        cls()
                        continue
                case 6:
                    raise KeyboardInterrupt

            time.sleep(2)
            cls()

        except ValueError:
            error_panel = Panel(
                "❌ [bold red]Invalid option selected[/bold red]",
                style="red"
            )
            console.print(error_panel)
            time.sleep(2)
            cls()
        except KeyboardInterrupt:
            console.print()
            with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
            ) as progress:
                progress.add_task(description="[yellow]Shutting down...", total=None)
                time.sleep(1.5)
            cls()
            exit(0)

if __name__ == '__main__':
    cls()
    print_header()

    # Красивая загрузка системы
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
    ) as progress:
        task = progress.add_task("[green]Initializing system...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.03)

    success_panel = Panel(
        "✅ [bold green]System initialized successfully![/bold green]",
        style="green",
        box=box.DOUBLE_EDGE
    )
    console.print(success_panel)
    time.sleep(1)
    cls()
    main()

