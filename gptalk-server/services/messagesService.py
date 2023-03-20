import json

from infrastructure.chatgpt import OpenaiClient
from config.configuration import OpenaiConfig
from infrastructure.db import IDatabase


class MessageService:
    def __init__(self, openai: OpenaiClient, db: IDatabase, config: OpenaiConfig):
        self.openai = openai
        self.db = db
        self.config = config

    def create_conversation(self) -> bool:
        conversation = {"role":"system", "content":self.config.behaviour}
        content = json.dumps(conversation)
        return self.db.add_new_chat(content)

    def get_conversation(self, chat_id):
        conversation = self.db.get_chat(chat_id)
        return conversation

    def handle_conversation(self, request: dict):
        response = self.openai.get_model_response(request)
        self.db.update_chat(response['chat_id'], json.dumps(response['messages']))
        return response

