import pytest
from unittest.mock import patch, Mock, AsyncMock
from app.chat import InitializedError, RateLimitError, NoChatsFoundError, APIError
from app.chat.chat_dto import ChatDto
from app.chat.chat_service import store_and_respond_chat, get_paginated_chats


@pytest.mark.asyncio
async def test_store_and_respond_chat_success(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history), \
            patch('app.chat.chat_service.CreateAgentAnswer') as mock_agent_class:
        # モックの設定を修正
        mock_agent_instance = Mock()
        mock_agent_instance.invoke_graph = AsyncMock(return_value=(
            # 適切なChatDtoインスタンスを返す
            ChatDto(answer="Test response", form=["item1"]),
            None
        ))
        mock_agent_class.return_value = mock_agent_instance

        # ここでCreateAgentAnswerクラスのinvoke_graph内で使用される
        # 変数名のマッピングを修正
        mock_agent_instance.select_chain = Mock()
        mock_agent_instance.select_chain.ainvoke = AsyncMock(return_value={
            'agent_options': '選択肢...',
            'chat_history': 'テスト履歴',
            'user_message': 'test message'
        })

        result = await store_and_respond_chat("test_user", "test message", False)
        assert isinstance(result, ChatDto)
        assert result.answer == "Test response"

@pytest.mark.asyncio
async def test_store_and_respond_chat_initialized_error():
    with patch('app.chat.chat_service.get_chat_history', return_value=None):
        with pytest.raises(InitializedError):
            await store_and_respond_chat("test_user", "test message", False)


@pytest.mark.asyncio
async def test_store_and_respond_chat_rate_limit(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history), \
            patch('app.chat.chat_service.CreateAgentAnswer') as mock_agent_class:
        mock_agent_instance = Mock()
        mock_agent_instance.invoke_graph = AsyncMock(
            side_effect=Exception("ResourceExhausted: 429")
        )
        mock_agent_class.return_value = mock_agent_instance

        with pytest.raises(RateLimitError):
            await store_and_respond_chat("test_user", "test message", False)


@pytest.mark.asyncio
async def test_store_and_respond_chat_api_error(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history), \
            patch('app.chat.chat_service.CreateAgentAnswer') as mock_agent_class:
        # モックの設定を修正
        mock_agent_instance = Mock()
        mock_agent_instance.invoke_graph = AsyncMock(side_effect=APIError("Test API Error"))
        mock_agent_class.return_value = mock_agent_instance

        with pytest.raises(APIError):
            await store_and_respond_chat("test_user", "test message", False)

# get_paginated_chatsのテスト
@pytest.mark.asyncio
async def test_get_paginated_chats_success(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history):
        result = await get_paginated_chats("test_user", 1, 10)
        assert isinstance(result, list)
        assert len(result) > 0
        assert 'message_id' in result[0]
        assert 'datetime' in result[0]
        assert 'message' in result[0]
        assert 'type' in result[0]

@pytest.mark.asyncio
async def test_get_paginated_chats_initialized_error():
    with patch('app.chat.chat_service.get_chat_history', return_value=None):
        with pytest.raises(InitializedError):
            await get_paginated_chats("test_user", 1)

@pytest.mark.asyncio
async def test_get_paginated_chats_no_chats_found(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history):
        with pytest.raises(NoChatsFoundError):
            await get_paginated_chats("test_user", 999)

@pytest.mark.asyncio
async def test_get_paginated_chats_error(mock_history):
    with patch('app.chat.chat_service.get_chat_history', return_value=mock_history) as mock_get:
        mock_get.side_effect = Exception("Unexpected error")
        with pytest.raises(Exception) as exc_info:
            await get_paginated_chats("test_user", 1)
        assert "Failed to retrieve chat history" in str(exc_info.value)