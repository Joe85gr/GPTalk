import json

from infrastructure.chatgpt import OpenaiClient
from config.configuration import OpenaiConfig
from infrastructure.db import IDatabase


class MessageService:
    def __init__(self, openai: OpenaiClient, db: IDatabase, config: OpenaiConfig):
        self.openai = openai
        self.db = db
        self.config = config

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
        return json.loads(conversation)

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
        self.db.update_chat(response['chat_id'], json.dumps(response))
        return response
