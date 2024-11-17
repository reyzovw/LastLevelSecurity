from sqlite3 import connect
from typing import Any
import os


class Core:
    def __init__(self, db_name_in_assets: str):
        if not os.path.exists("./.storage"):
            os.mkdir("./.storage")

        self.__connection = connect(f"./.storage/{db_name_in_assets}.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def execute_query(self, *args) -> list[Any] | None:
        self.__cursor.execute(*args)
        self.__connection.commit()

        return self.__cursor.fetchall()
