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
            models = [row['id'] for row in model_lst['data']]
            return models

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
            content = 'Error: Unable to connect to the server.'
            self.logger.error(f"OpenaiClient {content}", e)
        except AuthenticationError as e:
            content = 'Error: Unable to authenticate with openai.'
            self.logger.error(f"OpenaiClient {content}", e)
        except RateLimitError as e:
            content = f'Error: Model {request["model"]} is currently overloaded with other ' \
                      f'requests. '
            self.logger.error(f"OpenaiClient {content}", e)
        except Exception as e:
            content = f'Error: Unknown Error.'
            self.logger.error(f"OpenaiClient {content}", e)

        data = {
            "chat_id": request['chat_id'],
            "messages": request['messages'],
            "total_tokens": total_tokens
        }

        # role = "assistant"
        # content = "all good.."

        data['messages'].append({"role": role, "content": content})

        return data

    def get_chat_description(self, messages: [dict], model: str):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        content = None
        messages.append({"role": "user", "content": "tl;dr of this conversation. 3 words max."})

        try:
            self.logger.debug("Getting chat completition..")
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages)

            content = completion.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenaiClient {content}", e)

        return content
