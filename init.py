from features.utils.config import Config


config_parser = Config("config.ini")
VERSION = config_parser.get_value("VERSION", "INFORMATION")
RELEASE = config_parser.get_value("RELEASE", "INFORMATION")
AUTHOR = config_parser.get_value("AUTHOR", "INFORMATION")

