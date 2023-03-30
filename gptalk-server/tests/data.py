from collections import namedtuple

from pydantic import BaseModel

VALID_MODELS = {"data": [
    {
        "created": 1649358449,
        "id": "babbage",
        "object": "model",
        "owned_by": "openai",
        "parent": None,
        "permission": [
            {
                "allow_create_engine": False,
                "allow_fine_tuning": False,
                "allow_logprobs": True,
                "allow_sampling": True,
                "allow_search_indices": False,
                "allow_view": True,
                "created": 1669085501,
                "group": None,
                "id": "modelperm-49FUp5v084tBB49tC4z8LPH5",
                "is_blocking": False,
                "object": "model_permission",
                "organization": "*"
            }
        ],
        "root": "babbage"
    },
    {
        "created": 1649359874,
        "id": "davinci",
        "object": "model",
        "owned_by": "openai",
        "parent": None,
        "permission": [
            {
                "allow_create_engine": False,
                "allow_fine_tuning": False,
                "allow_logprobs": True,
                "allow_sampling": True,
                "allow_search_indices": False,
                "allow_view": True,
                "created": 1669066355,
                "group": None,
                "id": "modelperm-U6ZwlyAd0LyMk4rcMdz33Yc3",
                "is_blocking": False,
                "object": "model_permission",
                "organization": "*"
            }
        ],
        "root": "davinci"
    }],
    "object": "list"}

completion = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "some response.",
        "role": "assistant"
      }
    }
  ],
  "created": 1680081760,
  "id": "some-id",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 331,
    "prompt_tokens": 17,
    "total_tokens": 348
  }
}


class Message(BaseModel):
    content: str
    role: str


class Choice(BaseModel):
    finish_reason: str
    index: int
    message: Message


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Completion(BaseModel):
    created: int
    id: str
    model: str
    object: str
    usage: Usage
    choices: list[Choice]


VALID_COMPLETION = Completion(**completion)

REQUEST = {
    'messages':
        [
            {'role': 'system', 'content': 'talk like a bro, use markdown code highlighting'},
            {'role': 'user', 'content': 'yo'}
        ],
    'total_tokens': 0,
    'chat_id': 1,
    'model': 'gpt-3.5-turbo-0301',
    'chat_description': 'new chat'
}
