from features.utils.console import draw_string
from features.encryption.methods import *

from time import sleep
from random import choice
from colorama import Fore
import string


def testing_systems():
    master_password = "".join([choice(string.ascii_lowercase) for _ in range(11)])
    random_text = "".join([choice(string.ascii_lowercase) for _ in range(11)])

    draw_string("Testing AES-256 encryption\n", message_type="information")
    print("--------------------------------------\n")
    draw_string(f"Testing config: use_iv={Fore.RED}Off{Fore.RESET}, use_hmac={Fore.RED}Off{Fore.RESET}", message_type="information")

    try:
        aes = AESCipher(generate_static_code(master_password))
        raw = random_text

        encrypted_raw = aes.encrypt(raw, use_iv=False, use_hmac=False)
        decrypted_raw = aes.decrypt(encrypted_raw, use_iv=False, use_hmac=False)

        if decrypted_raw == raw:
            sleep(0.5)
            draw_string("Testing result: Everything is fine", message_type="success")
        else:
            draw_string("Test failed", message_type="error")
            exit(-1)

        print("\n--------------------------------------\n")

        draw_string(f"Testing config: use_iv={Fore.GREEN}On{Fore.RESET}, use_hmac={Fore.GREEN}On{Fore.RESET}",
                    message_type="information")

        encrypted_raw = aes.encrypt(raw)
        decrypted_raw = aes.decrypt(encrypted_raw)

        if decrypted_raw == raw:
            sleep(0.5)
            draw_string("Testing result: Everything is fine", message_type="success")
        else:
            draw_string("Test failed", message_type="error")
            exit(-1)
    except Exception as e:
        draw_string(f"An error occurred while testing AES-256 encryption, config: default, stacktrace: {e}",
                    message_type="error")



