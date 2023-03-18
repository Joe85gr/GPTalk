from pydantic import BaseModel


class OpenaiConfig(BaseModel):
    api_key: str


class Configuration(BaseModel):
    openai: OpenaiConfig
