import json
from logging import Logger

from infrastructure.cache import Cache
from infrastructure.chatgpt import OpenaiClient
from config.configuration import OpenaiConfig
from infrastructure.db import IDatabase


class MessageService:
    def __init__(self,
                 openai: OpenaiClient,
                 db: IDatabase,
                 config: OpenaiConfig,
                 logger: Logger,
                 cache: Cache):
        self.openai = openai
        self.db = db
        self.config = config
        self.logger = logger
        self.cache = cache
        self.models_key = "models"

    def get_models(self):
        cachedModels = self.cache.GetFromCache(self.models_key)
        if cachedModels is not None:
            self.logger.info("Found cached models!")
            models = json.loads(cachedModels)
        else:
            self.logger.info("No cached models found.")
            self.logger.info("Getting models from api..")
            models = self.openai.get_all_models()
            self.logger.info("Got Models! Caching them..")
            cached = self.cache.SetCache(self.models_key, json.dumps(models))
            if cached is True:
                self.logger.info("Cached models!")
            else:
                self.logger.error("Unable to cache models!")
        return models

    def create_conversation(self):
        modelBehaviour = {"role": "system", "content": self.config.behaviour}

        chat_id = self.db.add_new_chat()

        conversation = {
            "chat_id": chat_id,
            "total_tokens": 0,
            "messages": [modelBehaviour],
            "chat_description": "new chat"
        }

        self.db.update_chat(chat_id, json.dumps(conversation))

        return conversation

    def get_conversation(self, chat_id):
        conversation = self.db.get_chat(chat_id)
        if conversation is not None:
            return json.loads(conversation)
        return None

    def delete_conversation(self, chat_id):
        deleted = self.db.delete_chat(chat_id)
        return deleted

    def get_conversations(self):
        conversations = self.db.get_chats()
        data = []
        for conversation in conversations:
            data.append(json.loads(conversation))

        return data

    def handle_conversation(self, request: dict):
        response = self.openai.get_model_response(request)

        if "chat_description" not in response:
            messages = [m for m in request['messages']]
            model = request['model']
            response['chat_description'] = self.openai.get_chat_description(messages, model)

        self.db.update_chat(response['chat_id'], json.dumps(response))
        return response
