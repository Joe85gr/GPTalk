import os
from abc import ABC, abstractmethod
from logging import Logger

import openai
from openai.error import RateLimitError, AuthenticationError


class IOpenaiClient(ABC):
    @abstractmethod
    def get_all_models(self) -> dict:
        pass

    @abstractmethod
    def get_model_response(self, request):
        pass

    @abstractmethod
    def get_chat_description(self, messages: [dict], model: str):
        pass


class OpenaiClient(IOpenaiClient):
    def __init__(self, logger: Logger):
        self.logger = logger

    def get_all_models(self) -> dict:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        models = []
        reply = "success"

        try:
            self.logger.debug("Loading models..")
            model_lst = openai.Model.list()
            self.logger.debug("ModelService loaded!")
            models = [row['id'] for row in model_lst['data']]

        except AuthenticationError as e:
            self.logger.error(f"OpenaiClient authentication error: ", e)
            reply = f"AuthenticationError"
        except Exception as e:
            self.logger.error(f"OpenaiClient error: ", e)
            reply = "Exception"

        return {"models": models, "reply": reply}

    def get_model_response(self, request: dict):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        total_tokens = 0
        role = "error"
        try:
            self.logger.debug("Getting chat completition..")
            completion = openai.ChatCompletion.create(
                model=request['model'],
                messages=request['messages'])

            content = completion.choices[0].message.content
            total_tokens = completion.usage.total_tokens
            role = "assistant"
            self.logger.debug("Chat completition retrieved successfully!")
        except AuthenticationError as e:
            content = 'Error: Unable to authenticate with openai_client.'
            self.logger.error(f"OpenaiClient {content}", e)
        except RateLimitError as e:
            content = f'Error: Model {request["model"]} is currently overloaded with other ' \
                      f'requests.'
            self.logger.error(f"OpenaiClient {content}", e)
        except Exception as e:
            content = f'Error: Unknown Error.'
            self.logger.error(f"OpenaiClient {content}", e)

        data = {
            "chat_id": request['chat_id'],
            "messages": request['messages'],
            "total_tokens": total_tokens
        }

        data['messages'].append({"role": role, "content": content})

        return data

    def get_chat_description(self, messages: [dict], model: str):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        content = None

        try:
            self.logger.debug("Getting chat completion..")
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages)

            content = completion.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenaiClient {content}", e)

        return content
