import pytest
from unittest.mock import Mock, AsyncMock
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

@pytest.fixture
def mock_firestore_client():
    return Mock()

@pytest.fixture
def mock_chat_history():
    history = Mock(spec=FirestoreChatMessageHistory)
    history.messages = []
    return history

@pytest.fixture
def mock_normal_chat_factory(mock_chat_history):
    factory = Mock()
    factory.create_ans = AsyncMock()
    factory.add_user_message = AsyncMock()
    return factory