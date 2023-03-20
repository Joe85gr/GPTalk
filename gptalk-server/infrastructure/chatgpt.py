import os
from abc import ABC, abstractmethod
from logging import Logger

import openai
from openai.error import APIConnectionError, RateLimitError, AuthenticationError


class IOpenaiClient(ABC):
    @abstractmethod
    def get_all_models(self) -> list:
        pass

    @abstractmethod
    def get_model_response(self, request):
        pass


class OpenaiClient(IOpenaiClient):
    def __init__(self, logger: Logger):
        self.logger = logger

    def get_all_models(self) -> list:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            self.logger.debug("Loading models..")
            model_lst = openai.Model.list()
            self.logger.debug("ModelService loaded!")
            return model_lst['data']

        except (APIConnectionError, TimeoutError) as e:
            ex = e
            error_message = 'Unable to connect to the server.'
        except AuthenticationError as e:
            ex = e
            error_message = 'Unable to authenticate with openai.'
        except RateLimitError as e:
            ex = e
            error_message = 'Openai api is currently overloaded with other requests.'
        except Exception as e:
            ex = e
            error_message = 'Unknown Error.'

        self.logger.debug(f"OpenaiClient error: {error_message}", ex)
        return []

    def get_model_response(self, request: dict):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        total_tokens = 0
        role = "error"
        ex = None

        try:
            self.logger.debug("Getting chat completition..")
            completion = openai.ChatCompletion.create(
                model=request['model'],
                messages=request['messages'])

            content = completion.choices[0].message.content
            total_tokens = completion.usage.total_tokens
            role = "assistant"
            self.logger.debug("Chat completition retrieved successfully!")
        except (APIConnectionError, TimeoutError) as e:
            ex = e
            content = 'Error: Unable to connect to the server.'
        except AuthenticationError as e:
            ex = e
            content = 'Error: Unable to authenticate with openai.'
        except RateLimitError as e:
            ex = e
            content = f'Error: Model {request["model"]} is currently overloaded with other ' \
                       f'requests. '
        except Exception as e:
            ex = e
            content = f'Error: Unknown Error.'

        if ex:
            self.logger.error(f"OpenaiClient {content}", ex)

        data = {
            "chat_id": request['chat_id'],
            "messages": request['messages'],
            "total_tokens": total_tokens
        }

        data['messages'].append({"role": role, "content": content})

        return data
