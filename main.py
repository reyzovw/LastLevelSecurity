from features.encryption.methods import generate_static_code
from features.utils.console import draw_string
from features.screen.menu import render_gui, draw_art
from features.utils.file import *
from colorama import Fore
from time import sleep
from init import *


def draw_main_menu():
    draw_art()
    draw_string(f"Version: {VERSION} {RELEASE}")
    draw_string(f"Author: @{AUTHOR}")

    print("--------------------------------------")

    render_gui()
    return int(input("\n[ • ] Action number: "))


def main():
    os.system(f"title LLS / build #{VERSION} {RELEASE}")
    os.system("cls")

    while True:
        try:
            action_number = draw_main_menu()

            match action_number:
                case 1:
                    try:
                        try:
                            os.system("cls")
                            draw_art()

                            draw_string("Press Ctrl + C to go back\n")

                            directory = input("Data directory: ")
                            block_name = input("Block name: ")
                            master_password = generate_static_code(input("Master password: "))

                            run_encryption(directory + "/", block_name, master_password)

                            draw_string("The block was successfully encrypted", message_type="success")
                        except KeyboardInterrupt:
                            os.system("cls")
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while encrypting the block: {e}", message_type="error")
                case 2:
                    try:
                        try:
                            os.system("cls")
                            draw_art()
                            draw_string("Press Ctrl + C to go back\n")

                            directory = input("Block directory: ")
                            master_password = generate_static_code(input("Master password: "))

                            run_decryption(directory + "/", master_password)

                            draw_string("The block was successfully decrypted", message_type="success")
                        except KeyboardInterrupt:
                            os.system("cls")
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while decrypting the block: {e}", message_type="error")
                case 3:
                    try:
                        try:
                            os.system("cls")
                            draw_art()
                            draw_string("Press Ctrl + C to go back\n")

                            draw_string(f"1: Use initialization vector: {Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}")
                            draw_string(f"2: Use Hash-based Message Authentication Code: {Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}")

                            edit_id = int(input("\nAction number: "))
                        except KeyboardInterrupt:
                            os.system("cls")
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while editing settings: {e}", message_type="error")
                case 4:
                    raise KeyboardInterrupt

            sleep(3)
            os.system('cls')
        except ValueError:
            draw_string("Такой опции не существует", message_type="error")
            sleep(2)
            os.system("cls")
        except KeyboardInterrupt:
            print()
            draw_string("Shutting down", message_type="warning")
            sleep(1.5)
            os.system("cls")
            exit(0)


if __name__ == '__main__':
    main()
