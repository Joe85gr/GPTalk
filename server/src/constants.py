from os import path

ROOT_PATH = path.dirname(path.dirname(path.normpath(__file__)))

APP_NAME = "gptalk"
CONFIG_PATH = "./user_config"
CONFIG_FULL_PATH = f"{CONFIG_PATH}/config.yml"
LOGS_PATH = "./logs"
