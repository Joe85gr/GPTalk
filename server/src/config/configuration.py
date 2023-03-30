from pydantic import BaseModel


class GPTalkConfig(BaseModel):
    logging_level: str
    max_log_size: int
    origins: list[str]


class OpenaiConfig(BaseModel):
    behaviour: str


class Configuration(BaseModel):
    gptalk: GPTalkConfig
    openai: OpenaiConfig
