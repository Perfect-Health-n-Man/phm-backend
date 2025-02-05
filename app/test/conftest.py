

import pytest
from unittest.mock import Mock, AsyncMock

from quart import Quart

from app.chat import chat_bp
from app.chat.chat_repository import FirestoreChatMessageHistory


@pytest.fixture
def mock_history():
    # カスタムFirestoreChatMessageHistoryクラスのインスタンスをモック化
    history = Mock(spec=FirestoreChatMessageHistory)

    # messagesプロパティの設定
    messages = [
        Mock(
            type="human",
            content="test message",
            additional_kwargs={"datetime": "2024-01-01"}
        ),
        Mock(
            type="ai",
            content="test response",
            additional_kwargs={"datetime": "2024-01-01"}
        )
    ]
    history.messages = messages[-6:]

    # to_history_strメソッドの設定
    history.to_history_str.return_value = "\n".join(
        [f"'{msg.type}': {msg.content}" for msg in messages[-6:]]
    )

    # aget_messagesメソッドの設定
    history.aget_messages = AsyncMock(return_value=messages)

    return history

@pytest.fixture
def mock_chat_dto():
    from app.chat.chat_dto import ChatDto
    return ChatDto(
        answer="Test response",
        form=["form item 1", "form item 2"]
    )

@pytest.fixture
def app():
    app = Quart(__name__)
    app.register_blueprint(chat_bp)
    return app
