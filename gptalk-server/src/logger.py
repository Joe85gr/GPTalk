import logging.handlers
from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path

from constants import LOGS_PATH, APP_NAME
from config.configuration import GPTalkConfig


class IGPTalkLog(ABC):
    @abstractmethod
    def get_logger(self, name) -> Logger:
        pass


class GPTalkLog(IGPTalkLog):
    def __init__(self, config: GPTalkConfig):
        self.config = config

    def get_logger(self, name) -> Logger:

        logger = logging.getLogger(name)
        logger.setLevel(self.config.logging_level)
        log_full_path = f"{LOGS_PATH}/{APP_NAME}.log"
        max_log_size = self.config.max_log_size * 1024 * 1024

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        Path(LOGS_PATH).mkdir(parents=True, exist_ok=True)
        log_file = Path(log_full_path)
        log_file.touch(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_full_path,
            maxBytes=max_log_size,
            backupCount=3
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
