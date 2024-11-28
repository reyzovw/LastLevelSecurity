from features.db.passwords import PasswordsDatabase
from features.utils.config import JsonConfig
from features.utils.config import Config


config_parser = Config("config.ini")
json_parser = JsonConfig()
passwords = PasswordsDatabase()

VERSION = config_parser.get_value("VERSION", "INFORMATION")
RELEASE = config_parser.get_value("RELEASE", "INFORMATION")
AUTHOR = config_parser.get_value("AUTHOR", "INFORMATION")

