import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES


class Aes256Method(object):
    def __init__(self, key):
        """
        Class for encrypting and decrypting data using the AES-256 byte method
        :param key: master key
        """
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        """
        To encrypt data
        :param raw: data for encrypt
        :return: cipher text
        """
        raw = self.__pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        """
        To decrypt data
        :param enc: encrypted data for decrypt
        :return: decrypted raw
        """
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return Aes256Method.__unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def __pad(self, s):
        """
        Normalize text bytes
        :param s: string
        :return: normalized text bytes
        """
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s) - 1:])]
