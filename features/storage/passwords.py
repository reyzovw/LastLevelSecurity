from features.utils.config import JsonConfig
from features.encryption.methods import *
from features.utils.database import Core
from features.utils.models import *


class PasswordsDatabase(Core):
    def __init__(self):
        super().__init__("passwords")
        self.__user_config = JsonConfig()

        query = """
        CREATE TABLE IF NOT EXISTS passwords
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
        """

        self.execute_query(query)

    def add_password(self, name: str, real_value: str, master_password: str):
        query = """
        INSERT INTO passwords (name, value) VALUES (?, ?)
        """

        master_password = master_password
        cipher = AESCipher(master_password)

        n = cipher.encrypt(name).decode()
        v = cipher.encrypt(real_value).decode()

        self.execute_query(query, (n, v))

    def get_password(self, password_id: int) -> PasswordModel | None:
        query = """
        SELECT * FROM passwords
        WHERE id = ?
        """

        try:
            result = self.execute_query(query, (password_id, ))[0]

            return PasswordModel(result[0], result[1], result[2])
        except IndexError:
            return None

    def get_all_name_and_id(self) -> list[PasswordModel] | None:
        query = """
        SELECT id FROM passwords
        """

        try:
            all_id = self.execute_query(query)
            data = []

            for current_id in all_id:
                info = self.get_password(current_id[0])

                if info:
                    data.append(info)

            return data
        except IndexError:
            return None

    def remove_password(self, password_id: int):
        query = """
        DELETE FROM passwords
        WHERE id = ?
        """

        self.execute_query(query, (password_id, ))
