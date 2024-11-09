from features.encryption.methods import AESCipher
from shutil import rmtree
from time import sleep
import json
import os


def get_byte_code(directory: str):
    try:
        with open(directory, "r") as file:
            return file.read()
    except UnicodeDecodeError:
        pass


def scan_directory(directory: str):
    blocks = []

    for root, dirs, files in os.walk(directory):
        if root == directory:
            for folder in dirs:
                blocks.append({"folder": folder})
            for file in files:
                blocks.append({"file": file, "bytecode": get_byte_code(directory + file)})
        else:
            for folder in dirs:
                relative_folder = os.path.relpath(os.path.join(root, folder), directory)
                blocks.append({"folder": relative_folder})
            for file in files:
                relative_file = os.path.relpath(os.path.join(root, file), directory)
                blocks.append({"file": relative_file, "bytecode": get_byte_code(directory + relative_file)})

    return blocks


def run_encryption(directory_path: str, block_name: str, master_password: str):
    block_data = scan_directory(directory_path)

    output_data = {
        "block": {
            "insecure_path": directory_path,
            "block_data": block_data
        }
    }

    encryption = AESCipher(master_password)

    with open(f"{block_name}.cbc", 'w', encoding='utf-8') as json_file:
        encrypted_text = encryption.encrypt(json.dumps(output_data))

        json_file.write(encrypted_text.decode())

    try:
        rmtree(directory_path)
    except PermissionError:
        pass


def run_decryption(block_directory: str, master_password: str):
    block_directory = block_directory[:-1]
    encryption = AESCipher(master_password)

    with open(fr"{block_directory}", "r") as file:
        data = file.read()

        decryption_result = json.loads(encryption.decrypt(data))
        insecure_path = dict(decryption_result)['block']['insecure_path']

        if not os.path.exists(insecure_path):
            os.mkdir(insecure_path)

        for current_block_data in decryption_result['block']['block_data']:
            if "folder" in current_block_data.keys():
                block_type = "folder"
            else:
                block_type = "file"

            if block_type == "folder":
                os.mkdir(insecure_path + current_block_data['folder'])
            else:
                with open(insecure_path + current_block_data['file'], "w") as file_creator_thread:
                    try:
                        file_creator_thread.write(current_block_data['bytecode'])
                    except TypeError:
                        # if 'bytecode' is null
                        pass

    os.remove(block_directory)

