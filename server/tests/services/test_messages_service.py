from src.config.configuration import OpenaiConfig
from src.services.messages_service import MessageService
from tests.mocks import MockLogger, MockCache, MockOpenaiClient, MockDb


class Test_MessageService:
    def test_get_models(self):
        # Arrange
        expectedResult = ['model1', 'model2']
        config = OpenaiConfig(behaviour="")
        mockOpenai = MockOpenaiClient(models=['model1', 'model2'])

        sut = MessageService(mockOpenai, MockDb(), config, MockLogger(), MockCache())

        # Act
        result = sut.get_models()

        # Assess
        assert result == expectedResult

    def test_create_conversation_returns_conversation(self):
        # Arrange
        chat_id = 1
        expectedResult = {
            "chat_id": chat_id,
            "total_tokens": 0,
            "messages": [
                {'role': 'system', 'content': ''}
            ],
            "chat_description": "new chat"
        }

        config = OpenaiConfig(behaviour="")
        mockDb = MockDb(chat_id=chat_id)
        mockOpenai = MockOpenaiClient(models=['model1', 'model2'])

        sut = MessageService(mockOpenai, mockDb, config, MockLogger(), MockCache())

        # Act
        result = sut.create_conversation()

        # Assess
        assert result == expectedResult
