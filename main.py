import os

from features.encryption.methods import generate_static_code
from features.utils.console import draw_string
from features.screen.menu import render_gui
from features.utils.file import *
from time import sleep
from init import *


def main():
    os.system("cls")

    while True:
        try:
            draw_string(f"Version: {VERSION} {RELEASE}", message_type="information")
            draw_string(f"Author: @{AUTHOR}", message_type="information")

            print("--------------------------------------")

            render_gui()
            action_number = int(input("\n[ • ] Action number: "))

            match action_number:
                case 1:
                    try:
                        directory = input("Directory: ")
                        block_name = input("Block name: ")
                        master_password = generate_static_code(input("Master password: "))

                        run_encryption(directory + "/", block_name, master_password)

                        draw_string("The block was successfully encrypted", message_type="success")
                    except Exception as e:
                        draw_string(f"An error occurred while encrypting the block: {e}", message_type="error")
                case 2:
                    try:
                        directory = input("Block directory: ")
                        master_password = generate_static_code(input("Master password: "))

                        run_decryption(directory + "/", master_password)

                        draw_string("The block was successfully decrypted", message_type="success")
                    except Exception as e:
                        draw_string(f"An error occurred while decrypting the block: {e}", message_type="error")
                case 3:
                    break

            sleep(3)
            os.system('cls')
        except ValueError:
            draw_string("Такого варианта не существует", message_type="error")
            sleep(2)
            os.system("cls")


if __name__ == '__main__':
    main()

