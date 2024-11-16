from features.encryption.methods import generate_static_code
from features.utils.console import draw_string, cls
from features.screen.menu import render_gui, draw_art
from features.utils.file import *
from time import sleep, time
from colorama import Fore
from init import *


def draw_main_menu():
    draw_art()
    draw_string(f"Version: {VERSION} {RELEASE}")
    draw_string(f"Author: @{AUTHOR}")

    print("--------------------------------------")

    render_gui()
    return int(input("\n[ • ] Action number: "))


def open_settings(user_config_data: dict):
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back\n")

    iv_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['use_iv'][0] else f"{Fore.RED}[NO]{Fore.RESET}"
    hmac_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['use_hmac'][0] else f"{Fore.RED}[NO]{Fore.RESET}"

    iv_data = f" {Fore.LIGHTYELLOW_EX}({user_config_data['use_iv'][2]}){Fore.RESET}"
    hmac_data = f" {Fore.LIGHTYELLOW_EX}({user_config_data['use_hmac'][2]}){Fore.RESET}"

    compress_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['compress_blocks'][0] else f"{Fore.RED}[NO]{Fore.RESET}"
    compress_data = f" {Fore.LIGHTYELLOW_EX}({user_config_data['compress_blocks'][2]}){Fore.RESET}"

    draw_string(f"1: Use initialization vector: {iv_status + iv_data}")
    draw_string(f"2: Use Hash-based Message Authentication Code: {hmac_status + hmac_data}")
    draw_string(f"3: Compress blocks: {compress_status + compress_data}")

    edit_id = int(input("\nAction number: "))

    match edit_id:
        case 1:
            if user_config_data['use_iv'][0]:
                json_parser.edit_data("use_iv", [False, True, "Will be no randomization, 'Strong impact'"])
            else:
                json_parser.edit_data("use_iv", [True, True, "Will be no randomization, 'Strong impact'"])
        case 2:
            if user_config_data['use_hmac'][0]:
                json_parser.edit_data("use_hmac", [False, True, "Increase the file size, 'Improved security'"])
            else:
                json_parser.edit_data("use_hmac", [True, True, "Increase the file size, 'Improved security'"])
        case 3:
            if user_config_data['compress_blocks'][0]:
                json_parser.edit_data("compress_blocks", [False, True, "Reducing block size"])
            else:
                json_parser.edit_data("compress_blocks", [True, True, "Reducing block size"])

    draw_art()
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
                        try:
                            cls()
                            draw_art()

                            draw_string("Press Ctrl + C to go back\n")

                            directory = input("Data directory: ")
                            block_name = input("Block name: ")
                            master_password = generate_static_code(input("Master password: "))

                            print()
                            draw_string("Data encryption has started, please wait...")

                            run_encryption(directory + "/", block_name, master_password,
                                           hmac=user_config_data['use_hmac'][0], iv=user_config_data['use_iv'][0])

                            draw_string("The block was successfully encrypted", message_type="success")
                        except KeyboardInterrupt:
                            cls()
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while encrypting the block: {e}", message_type="error")
                case 2:
                    try:
                        try:
                            cls()
                            draw_art()
                            draw_string("Press Ctrl + C to go back\n")

                            directory = input("Block directory: ")
                            master_password = generate_static_code(input("Master password: "))

                            print()
                            draw_string("Data decryption has started, please wait...")

                            run_decryption(directory + "/", master_password, hmac=user_config_data['use_hmac'][0], iv=user_config_data['use_iv'][0])

                            draw_string("The block was successfully decrypted", message_type="success")
                        except KeyboardInterrupt:
                            cls()
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while decrypting the block: {e}", message_type="error")
                case 3:
                    try:
                        try:
                            open_settings(user_config_data)
                        except KeyboardInterrupt:
                            cls()
                            continue
                    except Exception as e:
                        e.with_traceback()
                        draw_string(f"An error occurred while editing settings: {e}", message_type="error")
                case 4:
                    raise KeyboardInterrupt

            sleep(3)
            cls()
        except ValueError:
            draw_string("Такой опции не существует", message_type="error")
            sleep(2)
            cls()
        except KeyboardInterrupt:
            print()
            draw_string("Shutting down", message_type="warning")
            sleep(1.5)
            cls()
            exit(0)


if __name__ == '__main__':
    main()
