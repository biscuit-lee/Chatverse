import pytest 
from unittest.mock import MagicMock

@pytest.fixture
def sample_post_response():
    return {
        "id": 1,
        "text": "Hello from my agent",
        "createdAt": "2024-06-01T12:00:00Z",
        "authorId": 42,
        "likes": 10,
        "dislikes": 2,
        "commentCount": 5,
        "profilePictureUrl": "https://example.com/profile.jpg",
    }

@pytest.fixture
def mock_client(sample_post_response):
    mock = MagicMock()
    mock.post.return_value = sample_post_response
    return mock