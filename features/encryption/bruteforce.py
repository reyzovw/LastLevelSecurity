from hashlib import sha256, md5, sha224, sha512, sha1
import os


class Bruteforce:
    def __init__(self, hash_id: int | str, target_hash: str):
        if not str(hash_id).isnumeric():
            raise TypeError("hash_id must be a integer")
        elif target_hash is None:
            raise TypeError(f"raw_hash cannot be a {type(target_hash)}, must be a str")

        self.__hash_obj: object = None
        self.__target_hash: str = target_hash
        self.__database_file = "data.txt"

        match hash_id:
            case 1:
                self.__hash_obj = sha256
            case 2:
                self.__hash_obj = md5
            case 3:
                self.__hash_obj = sha224
            case 4:
                self.__hash_obj = sha512
            case 5:
                self.__hash_obj = sha1

    def __get_hash(self, raw: str) -> str:
        return self.__hash_obj(raw.encode()).hexdigest()

    def __confirm_hash(self, raw: str) -> bool:
        raw_hash = self.__get_hash(raw)

        return raw_hash == self.__target_hash

    def run(self) -> dict:
        if not os.path.exists(self.__database_file):
            raise FileNotFoundError("data.txt not found")

        with open(self.__database_file, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.replace("\n", "").strip()
                confirm_result = self.__confirm_hash(word)

                if confirm_result:
                    return {"found": True, "word": word, "hash": self.__target_hash}

        return {"found": False}
