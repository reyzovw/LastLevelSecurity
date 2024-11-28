from configparser import ConfigParser
import json
import os


class Config:
    def __init__(self, config_filename: str):
        self._config = ConfigParser()
        self._config.read(config_filename)

    def get_value(self, option: str, section: str = 'GENERAL') -> str:
        value = self._config.get(
            section=section,
            option=option
        )
        return value


class JsonConfig:
    def __init__(self):
        self.__filename = ".db/user_config.json"
        self.__scheme = {
            "use_iv": [True, False, "Will be no randomization, 'Strong impact'"],
            "use_hmac": [True, False, "Increase the file size, 'Improved security'"],
            "compress_blocks": [False, True, "Reducing block size"]
        }

        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(self.__scheme, file, indent=4)

    def get_user_config_data(self) -> dict[str, [bool, bool]]:
        with open(self.__filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def edit_data(self, key: str, value: str):
        with open(self.__filename, "r", encoding="utf-8") as file:
            user_config_json = json.load(file)

        user_config_json[key] = value

        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(user_config_json, file)

