import hashlib
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import hmac


class AESCipher(object):
    def __init__(self, key):  # Изменено на __init__
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = pad(raw.encode(), self.bs)  # Используем pad из Crypto.Util.Padding
        iv = get_random_bytes(self.bs)  # Более безопасный способ генерации IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw)

        # Создаем HMAC для проверки целостности
        hmac_tag = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest()

        return base64.b64encode(iv + hmac_tag + encrypted)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:self.bs]
        hmac_tag = enc[self.bs:self.bs + 32]  # Длина HMAC для SHA-256 - 32 байта
        encrypted = enc[self.bs + 32:]

        # Проверяем HMAC
        if hmac.new(self.key, iv + encrypted, hashlib.sha256).digest() != hmac_tag:
            raise ValueError("Invalid HMAC! Data may have been tampered with.")

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted), self.bs).decode('utf-8')


def generate_static_code(input_text):
    hash_object = hashlib.md5(input_text.encode())
    hash_code = hash_object.hexdigest()

    static_code = ''.join(str(int(char, 16) % 9 + 1) for char in hash_code)[:16]

    return static_code

