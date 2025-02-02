import pytest
from unittest.mock import patch, Mock, AsyncMock
from app.chat import InitializedError, RateLimitError, NoChatsFoundError
from app.chat.chat_service import store_and_respond_chat, get_paginated_chats


@pytest.mark.asyncio
async def test_store_and_respond_chat_success(mock_chat_history):
    # 正常系のテスト
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_chat_history), \
            patch('app.chat.chat_service.NormalChatFactory') as mock_factory_class:
        mock_factory = Mock()
        mock_factory.create_ans = AsyncMock(return_value=Mock(
            model_dump=lambda: {'answer': 'test answer', 'form': None}
        ))
        mock_factory_class.return_value = mock_factory

        result = await store_and_respond_chat("test_uid", "test message")
        assert result == {'answer': 'test answer'}


@pytest.mark.asyncio
async def test_store_and_respond_chat_initialize_error():
    with patch('app.chat.chat_service.get_chat_history', return_value=None):
        with pytest.raises(InitializedError) as exc_info:
            await store_and_respond_chat("test_uid", "test message")
        assert "Failed to initialize chat history" in str(exc_info.value)


@pytest.mark.asyncio
async def test_store_and_respond_chat_rate_limit(mock_chat_history):
    # レート制限エラーのテスト
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_chat_history), \
            patch('app.chat.chat_service.NormalChatFactory') as mock_factory_class:
        mock_factory = Mock()
        mock_factory.create_ans = AsyncMock(side_effect=Exception("ResourceExhausted: 429"))
        mock_factory_class.return_value = mock_factory

        with pytest.raises(RateLimitError) as exc_info:
            await store_and_respond_chat("test_uid", "test message")
        assert "Rate limit exceeded" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_paginated_chats_success(mock_chat_history):
    # ページネーションの正常系テスト
    mock_messages = [
        Mock(
            additional_kwargs={'datetime': '2024-01-01'},
            content='test message',
            type='human'
        )
    ]
    mock_chat_history.aget_messages = AsyncMock(return_value=mock_messages)

    with patch('app.chat.chat_service.get_chat_history', return_value=mock_chat_history):
        result = await get_paginated_chats("test_uid", 1)
        assert len(result) == 1
        assert result[0]['message'] == 'test message'


@pytest.mark.asyncio
async def test_get_paginated_chats_initialize_error():
    with patch('app.chat.chat_service.get_chat_history', return_value=None):
        with pytest.raises(InitializedError) as exc_info:
            await get_paginated_chats("test_uid", 1)
        assert "Failed to initialize chat history" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_paginated_chats_not_found(mock_chat_history):
    mock_chat_history.aget_messages = AsyncMock(return_value=[])
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_chat_history):
        with pytest.raises(NoChatsFoundError) as exc_info:
            await get_paginated_chats("test_uid", 2)
        assert "No chats found for the specified page" in str(exc_info.value)