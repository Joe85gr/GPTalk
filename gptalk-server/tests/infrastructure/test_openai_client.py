import pytest
from openai.error import AuthenticationError, RateLimitError
from src.infrastructure.openai_client import OpenaiClient
from tests.data import VALID_MODELS, REQUEST, get_valid_completion
from tests.mocks import MockLogger

modelsExceptionsTestData = [
    (Exception(), {'models': [], 'reply': 'Exception'}),
    (AuthenticationError(), {'models': [], 'reply': 'AuthenticationError'}),
]

completionExceptionsTestData = [
    (Exception(), {'role': 'error', 'content': 'Error: Unknown Error.'}),
    (AuthenticationError(), {'role': 'error', 'content': 'Error: Unable to authenticate with openai_client.'}),
    (RateLimitError(), {
        'role': 'error',
        'content': f'Error: Model {REQUEST["model"]} is currently overloaded with other requests.'}),
]

sut = OpenaiClient(MockLogger())


class Test_OpenaiClient:
    def test_get_all_models_returns_models(self, mocker):
        # Arrange
        expectedResult = {'models': ['babbage', 'davinci'], 'reply': 'success'}
        models = VALID_MODELS
        mocker.patch("openai.api_key")
        mocker.patch("openai.Model.list", return_value=models)

        # Act
        result = sut.get_all_models()

        # Assess
        assert result == expectedResult

    @pytest.mark.parametrize("exception, expected_result", modelsExceptionsTestData)
    def test_when_exception_is_thrown_get_all_models_returns_reply_exception(self, exception, expected_result, mocker):
        # Arrange
        mocker.patch("openai.api_key")
        mocker.patch("openai.Model.list", side_effect=exception)

        # Act
        result = sut.get_all_models()

        # Assess
        assert result == expected_result

    def test_get_model_response_appends_assistant_reply_to_messages(self, mocker):
        # Arrange
        newContent = 'some content.'
        expectedResult = {
            'chat_id': 1,
            'messages':
                [
                    {'role': 'system', 'content': 'talk like a bro, use markdown code highlighting'},
                    {'role': 'user', 'content': 'yo'},
                    {'role': 'assistant', 'content': newContent}],
            'total_tokens': 348
        }

        completion = get_valid_completion(newContent)

        mocker.patch("openai.ChatCompletion.create", return_value=completion)

        # Act
        result = sut.get_model_response(REQUEST)

        # Assess
        assert result == expectedResult

    @pytest.mark.parametrize("exception, expected_result", completionExceptionsTestData)
    def test_when_exception_is_thrown_get_model_response_appends_error_reply_to_messages(self,
                                                                                         exception,
                                                                                         expected_result: dict,
                                                                                         mocker):
        # Arrange
        mocker.patch("openai.ChatCompletion.create", side_effect=exception)

        # Act
        result = sut.get_model_response(REQUEST)

        # Assert
        assert result['messages'][-1] == expected_result

    def test_get_chat_description_returns_description(self, mocker):
        # Arrange
        expectedResult = "some-tldr."
        request = [{"role": "user", "content": f"tl;dr of the following text, max 3 words: \nsome-conversation"}]

        completion = get_valid_completion(expectedResult)

        mocker.patch("openai.ChatCompletion.create", return_value=completion)

        # Act
        result = sut.get_chat_description(request, "some-model")

        # Assert
        assert result == expectedResult

    def test_when_exception_is_thrown_get_chat_description_returns_none(self, mocker):
        # Arrange
        expectedResult = None
        request = [{"role": "user", "content": f"tl;dr of the following text, max 3 words: \nsome-conversation"}]

        mocker.patch("openai.ChatCompletion.create", side_effect=Exception())

        # Act
        result = sut.get_chat_description(request, "some-model")

        # Assert
        assert result == expectedResult
