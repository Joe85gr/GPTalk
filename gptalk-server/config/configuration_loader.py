from config.configuration import Configuration
from yaml import safe_load
from constants import CONFIG_FULL_PATH


class ConfigLoader:
    @staticmethod
    def get_config() -> Configuration:
        with open(CONFIG_FULL_PATH, "r") as file:
            rawConfig = safe_load(file)

        return Configuration(**rawConfig)
