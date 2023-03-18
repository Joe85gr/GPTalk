import os
import openai
from openai.error import APIConnectionError, RateLimitError, AuthenticationError
from config.configuration import OpenaiConfig


class OpenaiClient:
    # def __init__(self):
        # self.config = config


    def get_all_models(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        model_lst = openai.Model.list()
        models = [x['id'] for x in model_lst['data']]

        data = {"models": models}

        return data

    def get_model_response(self, request):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        total_tokens = 0
        role = "error"

        try:
            completion = openai.ChatCompletion.create(
                model=request['model'],
                messages=request['messages'])
            response = completion.choices[0].message.content
            total_tokens = completion.usage.total_tokens
            role = "assistant"

        except (APIConnectionError, TimeoutError):
            response = 'Error: Unable to connect to the server.'
        except AuthenticationError:
            response = 'Error: Unable to authenticate with openai.'
        except RateLimitError:
            response = f'Error: Model {request["model"]} is currently overloaded with other ' \
                       f'requests. '
        except:
            response = f'Error: Unknown Error.'

        request['messages'].append({"role": role, "content": response})

        data = {"messages": request['messages'], "total_tokens": total_tokens}

        return data
