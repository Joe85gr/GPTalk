from logging import Logger

from src.infrastructure.cache import ICache
from src.infrastructure.db import IDatabase
from src.infrastructure.openai_client import IOpenaiClient


class MockLogger(Logger):
    def __init__(self, name: str = "test"):
        super().__init__(name)

    def debug(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass


class MockCache(ICache):
    def __init__(self, get_from_cache: str = None, set_cache=None):
        self.get_from_cache = get_from_cache
        self.set_cache = set_cache

    def GetFromCache(self, key: str):
        return self.get_from_cache

    def SetCache(self, key: str, value: str, timeout: int = 0):
        return self.set_cache


class MockOpenaiClient(IOpenaiClient):
    def __init__(self, models=None):
        self.models = models

    def get_all_models(self) -> dict:
        return self.models

    def get_model_response(self, request):
        pass

    def get_chat_description(self, messages: [dict], model: str):
        pass


class MockDb(IDatabase):
    def __init__(self, chat_id=None):
        self.chat_id = chat_id

    def add_new_chat(self) -> str:
        return self.chat_id

    def get_chat(self, chat_id):
        pass

    def delete_chat(self, chat_id):
        pass

    def get_chats(self):
        pass

    def update_chat(self, chat_id, content) -> bool:
        pass
