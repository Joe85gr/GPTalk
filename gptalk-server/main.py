import uvicorn
import sqlite3

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from infrastructure.chatgpt import OpenaiClient
from config.configuration_loader import ConfigLoader
from logger import GPTalkLog
from infrastructure.db import Sqlite
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


@app.post("/api/handle_conversation")
async def handle_conversation(request: Request):
    _logger.info("Processing request 'messages'..")
    data = _messageService.handle_conversation(await request.json())
    return data


@app.get("/api/conversations/")
async def get_conversation(chat_id: int | None = None):
    _logger.info(f"Getting conversation with chat id:{chat_id}..")
    data = _messageService.get_conversations()
    return data


@app.get("/api/conversations/{chat_id}")
async def get_conversation(chat_id: int):
    _logger.info(f"Getting conversation with chat id:{chat_id}..")
    data = _messageService.get_conversation(chat_id)
    if data is None:
        raise HTTPException(status_code=404, detail="chat_id not found")
    return data


@app.delete("/api/conversations/{chat_id}")
async def delete_conversation(chat_id: int):
    _logger.info(f"Deleting conversation with chat id:{chat_id}..")
    deleted = _messageService.delete_conversation(chat_id)
    return {"deleted": deleted}


@app.post("/api/new_chat")
async def create_new_chat():
    _logger.info("Adding new chat..")
    conversation = _messageService.create_conversation()
    return conversation


@app.get("/api/models")
async def get_models():
    _logger.info("Processing request 'models'..")
    models = _client.get_all_models()
    return {"models": models}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
