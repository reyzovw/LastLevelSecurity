from colorama import Fore
from typing import Literal


def draw_string(string: str,
                message_type: Literal["default", "information", "warning", "error", "success"] = "default"):

    match message_type:
        case "default":
            print(f"{Fore.LIGHTWHITE_EX}[ • ] {string}")
        case "information":
            print(f"{Fore.WHITE}[ • ]{Fore.RESET} {string}")
        case "warning":
            print(f"{Fore.YELLOW}[ • ]{Fore.RESET} {string}")
        case "error":
            print(f"{Fore.RED}[ • ]{Fore.RESET} {string}")
        case "success":
            print(f"{Fore.GREEN}[ • ]{Fore.RESET} {string}")
