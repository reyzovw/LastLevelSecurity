import hashlib
import hmac
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw, use_iv=True, use_hmac=True):
        raw = pad(raw.encode(), self.bs)
        iv = get_random_bytes(self.bs) if use_iv else b'\x00' * self.bs  # Заменяем на нули, если не использовать IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw)

        hmac_tag = hmac.new(self.key, iv + encrypted, hashlib.sha256).digest() if use_hmac else b''

        return base64.b64encode(iv + hmac_tag + encrypted) if use_iv or use_hmac else base64.b64encode(encrypted)

    def decrypt(self, enc, use_iv=True, use_hmac=True):
        enc = base64.b64decode(enc)

        if use_iv:
            iv = enc[:self.bs]
            offset = self.bs
        else:
            iv = b'\x00' * self.bs
            offset = 0

        hmac_tag = enc[offset:offset + 32] if use_hmac else b''
        encrypted = enc[offset + (32 if use_hmac else 0):]

        if use_hmac and hmac.new(self.key, iv + encrypted, hashlib.sha256).digest() != hmac_tag:
            raise ValueError("Invalid HMAC! Data may have been tampered with.")

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted), self.bs).decode('utf-8')


def generate_static_code(input_text):
    hash_object = hashlib.md5(input_text.encode())
    hash_code = hash_object.hexdigest()

    static_code = ''.join(str(int(char, 16) % 9 + 1) for char in hash_code)[:16]

    return static_code
