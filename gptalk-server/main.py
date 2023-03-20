import uvicorn

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from infrastructure.chatgpt import OpenaiClient
from config.configuration_loader import ConfigLoader
from logger import GPTalkLog
from infrastructure.db import Sqlite
import sqlite3
from services.messagesService import MessageService

app = FastAPI()

_config = ConfigLoader.get_config()
_logger = GPTalkLog(_config.gptalk).get_logger('__main__')
_client = OpenaiClient(_logger)
_db = Sqlite(_logger, sqlite3)
_messageService = MessageService(_client, _db, _config.openai)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/*",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3000/*",
    "http://172.20.0.11",
    "http://172.20.0.11/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/messages")
async def handle_conversation(request: Request):
    _logger.info("Processing request 'messages'..")
    data = _messageService.handle_conversation(await request.json())
    return data


@app.post("/api/new_chat")
async def create_new_chat():
    _logger.info("Adding new chat..")
    new_chat_id = _messageService.create_conversation()
    return { "chat_id": new_chat_id }

@app.get("/api/models")
async def get_models():
    _logger.info("Processing request 'models'..")
    data = _client.get_all_models()
    return data


@app.get("/api/conversation/{chat_id}")
async def get_conversation(chat_id: int):
    _logger.info(f"Getting conversation with chat id:{chat_id}..")
    data = _messageService.get_conversation(chat_id)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
