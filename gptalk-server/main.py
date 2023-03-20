import uvicorn

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from api.chatgpt import OpenaiClient
from config.configuration_loader import ConfigLoader
from logger import GPTalkLog

app = FastAPI()

_config = ConfigLoader.get_config()
_logger = GPTalkLog(_config.gptalk).get_logger('__main__')
_client = OpenaiClient()


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
async def create_messages(request: Request):
    _logger.info("Processing request 'messages'..")
    data = _client.get_model_response(await request.json())
    return data


@app.get("/api/models")
async def get_models():
    _logger.info("Processing request 'models'..")
    data = _client.get_all_models()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
