from logging import Logger

import pytest
from openai.error import AuthenticationError, RateLimitError

from src.infrastructure.openai_client import OpenaiClient
from tests.data import VALID_MODELS, VALID_COMPLETION, REQUEST


class MockLogger(Logger):
    def __init__(self, name: str = "test"):
        super().__init__(name)

    def debug(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass


modelsExceptionsTestData = [
    (Exception(), {'models': [], 'reply': 'Exception'}),
    (AuthenticationError(), {'models': [], 'reply': 'AuthenticationError'}),
]

completionExceptionsTestData = [
    (Exception(), {'role': 'error', 'content': 'Error: Unknown Error.'}),
    (AuthenticationError(), {'role': 'error', 'content': 'Error: Unable to authenticate with openai.'}),
    (RateLimitError(), {
        'role': 'error',
        'content': f'Error: Model {REQUEST["model"]} is currently overloaded with other requests.'}),
]


class Test_OpenaiClient:
    def test_get_all_models_returns_models(self, mocker):
        # Arrange
        expectedResult = {'models': ['babbage', 'davinci'], 'reply': 'success'}
        models = VALID_MODELS
        mocker.patch("openai.api_key")
        mocker.patch("openai.Model.list", return_value=models)
        sut = OpenaiClient(MockLogger())

        # Act
        result = sut.get_all_models()

        # Assess
        assert result == expectedResult

    @pytest.mark.parametrize("exception, expected_result", modelsExceptionsTestData)
    def test_when_exception_is_thrown_get_all_models_returns_reply_exception(self, exception, expected_result, mocker):
        # Arrange
        mocker.patch("openai.api_key")
        mocker.patch("openai.Model.list", side_effect=exception)
        sut = OpenaiClient(MockLogger())

        # Act
        result = sut.get_all_models()

        # Assess
        assert result == expected_result

    def test_get_model_response_appends_assistant_reply_to_messages(self, mocker):
        # Arrange
        expectedResult = {
            'chat_id': 1,
            'messages':
                [
                    {'role': 'system', 'content': 'talk like a bro, use markdown code highlighting'},
                    {'role': 'user', 'content': 'yo'},
                    {'role': 'assistant', 'content': 'some response.'}],
            'total_tokens': 348
        }

        mocker.patch("openai.ChatCompletion.create", return_value=VALID_COMPLETION)
        sut = OpenaiClient(MockLogger())

        result = sut.get_model_response(REQUEST)

        assert result == expectedResult

    @pytest.mark.parametrize("exception, expected_result", completionExceptionsTestData)
    def test_when_exception_is_thrown_get_model_response_appends_error_reply_to_messages(self,
                                                                                         exception,
                                                                                         expected_result: dict,
                                                                                         mocker):
        # Arrange
        mocker.patch("openai.ChatCompletion.create", side_effect=exception)
        sut = OpenaiClient(MockLogger())

        result = sut.get_model_response(REQUEST)

        assert result['messages'][-1] == expected_result
