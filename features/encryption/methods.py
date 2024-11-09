import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES


class AESCipher(object):
    def __init__(self, key):  # Исправлено на __init__
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = iv + cipher.encrypt(raw.encode())
        return base64.b64encode(encrypted)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def generate_static_code(input_text):
    hash_object = hashlib.md5(input_text.encode())
    hash_code = hash_object.hexdigest()

    static_code = ''.join(str(int(char, 16) % 9 + 1) for char in hash_code)[:16]

    return static_code

