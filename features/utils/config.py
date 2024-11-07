from configparser import ConfigParser


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

