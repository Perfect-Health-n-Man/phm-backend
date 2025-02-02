import pytest
from unittest.mock import patch, AsyncMock
from quart import g

from app.chat import InitializedError, RateLimitError, NoChatsFoundError, APIError
from app.chat.chat_dto import ChatDto


@pytest.mark.asyncio
async def test_handle_chat_success(app, mock_chat_dto):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(return_value=mock_chat_dto)):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 201
                response_data = await response.get_json()
                assert response_data['answer'] == "Test response"
                assert response_data['form'] == ["form item 1", "form item 2"]

@pytest.mark.asyncio
async def test_handle_chat_without_form(app):
    chat_dto = ChatDto(answer="Test response", form=[])
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(return_value=chat_dto)):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 201
                response_data = await response.get_json()
                assert response_data['answer'] == "Test response"
                assert response_data['form'] == []

@pytest.mark.asyncio
async def test_handle_chat_missing_user_id(app):
    async with app.test_client() as client:
        async with app.app_context():
            response = await client.post('/', json={'message': 'test'})
            assert response.status_code == 400
            response_data = await response.get_json()
            assert 'error' in response_data

@pytest.mark.asyncio
async def test_handle_chat_missing_message(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            response = await client.post('/', json={})
            assert response.status_code == 400

@pytest.mark.asyncio
async def test_handle_chat_initialized_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(side_effect=InitializedError("Init error"))):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 500

@pytest.mark.asyncio
async def test_handle_chat_rate_limit(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(side_effect=RateLimitError("Rate limit"))):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 429

@pytest.mark.asyncio
async def test_handle_chat_api_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(side_effect=APIError("API error"))):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 500

# GETエンドポイントのテスト
@pytest.mark.asyncio
async def test_get_chat_list_success(app):
    test_chats = [{'message_id': 1, 'message': 'test'}]
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(return_value=test_chats)):
                response = await client.get('/?pages=1')
                assert response.status_code == 200
                response_data = await response.get_json()
                assert 'chats' in response_data
                assert response_data['page'] == 1

@pytest.mark.asyncio
async def test_get_chat_list_missing_user_id(app):
    async with app.test_client() as client:
        async with app.app_context():
            response = await client.get('/?pages=1')
            assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_chat_list_not_found(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(side_effect=NoChatsFoundError("Not found"))):
                response = await client.get('/?pages=999')
                assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_chat_list_initialized_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(side_effect=InitializedError("Init error"))):
                response = await client.get('/?pages=1')
                assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_chat_list_unexpected_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(side_effect=Exception("Unexpected"))):
                response = await client.get('/?pages=1')
                assert response.status_code == 500