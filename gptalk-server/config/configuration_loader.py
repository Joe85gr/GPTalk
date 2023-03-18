from abc import ABC, abstractmethod

from config.configuration import Configuration
from yaml import safe_load


class IConfigLoader(ABC):
    @staticmethod
    @abstractmethod
    def set_config() -> str:
        pass


class ConfigLoader(IConfigLoader):
    @staticmethod
    def set_config() -> Configuration:
        try:
            with open(f"./user_config/config.yml", "r") as file:
                rawConfig = safe_load(file)

            return Configuration(**rawConfig)
        except:
            return Configuration()
