from pydantic import BaseModel


class GPTalkConfig(BaseModel):
    logging_level: str
    max_log_size: int
    client_address: str

class OpenaiConfig(BaseModel):
    behaviour: str

class Configuration(BaseModel):
    gptalk: GPTalkConfig
    openai: OpenaiConfig
