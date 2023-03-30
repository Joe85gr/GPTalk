from tests.helpers import Completion

VALID_MODELS = {"data": [
    {
        "created": 1649358449,
        "id": "babbage",
        "object": "model",
        "owned_by": "openai_client",
        "parent": None,
        "permission": [
            {
                "allow_create_engine": False,
                "allow_fine_tuning": False,
                "allow_logprobs": True,
                "allow_sampling": True,
                "allow_search_indices": False,
                "allow_view": True,
                "created": 1669085501,
                "group": None,
                "id": "modelperm-49FUp5v084tBB49tC4z8LPH5",
                "is_blocking": False,
                "object": "model_permission",
                "organization": "*"
            }
        ],
        "root": "babbage"
    },
    {
        "created": 1649359874,
        "id": "davinci",
        "object": "model",
        "owned_by": "openai_client",
        "parent": None,
        "permission": [
            {
                "allow_create_engine": False,
                "allow_fine_tuning": False,
                "allow_logprobs": True,
                "allow_sampling": True,
                "allow_search_indices": False,
                "allow_view": True,
                "created": 1669066355,
                "group": None,
                "id": "modelperm-U6ZwlyAd0LyMk4rcMdz33Yc3",
                "is_blocking": False,
                "object": "model_permission",
                "organization": "*"
            }
        ],
        "root": "davinci"
    }],
    "object": "list"}


def get_valid_completion(content):
    rawCompletion = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": f"{content}",
                    "role": "assistant"
                }
            }
        ],
        "created": 1680081760,
        "id": "some-id",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": 331,
            "prompt_tokens": 17,
            "total_tokens": 348
        }
    }

    return Completion(**rawCompletion)


REQUEST = {
    'messages':
        [
            {'role': 'system', 'content': 'talk like a bro, use markdown code highlighting'},
            {'role': 'user', 'content': 'yo'}
        ],
    'total_tokens': 0,
    'chat_id': 1,
    'model': 'gpt-3.5-turbo-0301',
    'chat_description': 'new chat'
}
