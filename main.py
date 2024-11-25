from features.encryption.methods import generate_static_code
from features.utils.console import draw_string, cls
from features.encryption.bruteforce import Bruteforce
from features.screen.menu import render_gui, draw_art
from features.utils.testing import testing_systems
from features.utils.file import *
from colorama import Fore
from time import sleep
from init import *


def draw_bruteforce_menu():
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back\n")

    draw_string("1: SHA-256", message_type='information')
    draw_string("2: MD-5", message_type='information')
    draw_string("3: SHA-224", message_type='information')
    draw_string("4: SHA-512", message_type='information')
    draw_string("5: SHA-1", message_type='information')

    hash_type = int(input("\n[ • ] Hash type: "))
    target_hash = str(input("[ • ] Hash value: "))

    bruteforce = Bruteforce(hash_type, target_hash)

    result = bruteforce.run()

    cls()
    draw_art()
    draw_string("Press Ctrl + C to stop bruteforce\n")

    if result['found']:
        draw_string(f"Decrypted value: {result['word']}", message_type='success')
        draw_string(f"Original hash: {result['hash']}", message_type='success')
    else:
        draw_string("Not found hash value :(", message_type='error')

    print()
    draw_string("Press Enter to go back")
    input()


def draw_main_menu():
    draw_art()
    draw_string(f"Version: {VERSION} {RELEASE}")
    draw_string(f"Author: @{AUTHOR}")

    print("--------------------------------------")

    render_gui()
    return int(input("\n[ • ] Action number: "))


def add_password_callback(password_head: str, master_password: str):
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back")

    password_value = input("\nPassword value: ")

    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back")
    yes_or_no = input("\nDo you really want to create such a password? [y/n]: ").lower()

    if yes_or_no == "y":
        passwords.add_password(password_head, password_value, master_password)
        sleep(0.5)
        draw_string("Password created successfully", message_type="success")
        sleep(1)
        open_password_manager(master_password)
    else:
        raise KeyboardInterrupt


def open_password_data(cipher: AESCipher, password_id: int, msp: str):
    try:
        cls()
        draw_art()
        draw_string("Press Ctrl + C to go back")
        print("--------------------------------------")
        draw_string("1 - Remove\n")

        data = passwords.get_password(password_id)

        if data:
            decrypted_data = PasswordModel(
                id=data.id,
                name=cipher.decrypt(data.name),
                value=cipher.decrypt(data.value)
            )

            draw_string(f"ID: {decrypted_data.id}", message_type="warning")
            draw_string(f"Head: {decrypted_data.name}", message_type="warning")
            draw_string(f"Data: {decrypted_data.value}", message_type="warning")

            action_number = int(input("\n[ • ] Action number: "))

            match action_number:
                case 1:
                    cls()
                    draw_art()
                    draw_string("Press Ctrl + C to go back")
                    yes_or_no = input("\nDo you really want this? [y/n]: ").lower()

                    if yes_or_no == "y":
                        passwords.remove_password(password_id)
                        draw_string(f"Password #{password_id} was successfully removed", message_type='success')
                        raise KeyboardInterrupt
                    else:
                        draw_string("No password found with this ID", message_type='error')

        else:
            draw_string("No such password exists", message_type="error")
            sleep(1.5)
            raise KeyboardInterrupt
    except KeyboardInterrupt:
        open_password_manager(msp)


def open_password_manager(master_password: str):
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back")
    print("--------------------------------------")
    draw_string("a - Add password; Enter the password ID to edit data\n")

    all_passwords = passwords.get_all_name_and_id()
    aes = AESCipher(master_password)

    all_indexes = []

    for data in all_passwords:
        index = data.id
        name_of_part = aes.decrypt(data.name)
        all_indexes.append(index)

        draw_string(f"{index}: {name_of_part}")

    edit_id = input("\nAction or password ID: ")

    if str(edit_id).isnumeric():
        if int(edit_id) in all_indexes:
            open_password_data(aes, edit_id, master_password)
        else:
            draw_string("No password found for this ID", message_type='error')
            sleep(1.5)
            open_password_manager(master_password)
    elif edit_id == "a":
        cls()
        draw_art()
        draw_string("Press Ctrl + C to go back")

        password_head = input("\nPassword head: ")

        add_password_callback(password_head, master_password)


def enter_to_password_manager():
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back\n")

    master_password = generate_static_code(input("Enter your master password: "))
    print(master_password)

    try:
        open_password_manager(master_password)
    except ValueError:
        draw_string(f"Master password is incorrect", message_type="error")


def open_settings(user_config_data: dict):
    cls()
    draw_art()
    draw_string("Press Ctrl + C to go back\n")

    iv_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['use_iv'][
        0] else f"{Fore.RED}[NO]{Fore.RESET}"
    hmac_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['use_hmac'][
        0] else f"{Fore.RED}[NO]{Fore.RESET}"

    iv_data = f" {Fore.LIGHTYELLOW_EX}({user_config_data['use_iv'][2]}){Fore.RESET}"
    hmac_data = f" {Fore.LIGHTYELLOW_EX}({user_config_data['use_hmac'][2]}){Fore.RESET}"

    compress_status = f"{Fore.LIGHTGREEN_EX}[YES]{Fore.RESET}" if user_config_data['compress_blocks'][
        0] else f"{Fore.RED}[NO]{Fore.RESET}"
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

                            run_decryption(directory + "/", master_password, hmac=user_config_data['use_hmac'][0],
                                           iv=user_config_data['use_iv'][0])

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
                        draw_string(f"An error occurred while opening settings: {e}", message_type="error")
                case 4:
                    try:
                        try:
                            enter_to_password_manager()
                        except KeyboardInterrupt:
                            cls()
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while opening password manager: {e}", message_type="error")
                case 5:
                    try:
                        try:
                            draw_bruteforce_menu()
                        except KeyboardInterrupt:
                            cls()
                            continue
                    except Exception as e:
                        draw_string(f"An error occurred while start bruteforce hash: {e}", message_type="error")
                case 6:
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
    cls()
    draw_art()
    testing_systems()
    sleep(1.5)
    cls()
    main()
