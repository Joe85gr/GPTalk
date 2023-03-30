from pydantic import BaseModel


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