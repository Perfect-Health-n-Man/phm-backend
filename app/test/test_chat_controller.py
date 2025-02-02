import pytest
from unittest.mock import patch, AsyncMock
from quart import Quart, g
from app.chat import chat_bp, RateLimitError, NoChatsFoundError, InitializedError

@pytest.fixture
def app():
    app = Quart(__name__)
    app.register_blueprint(chat_bp)
    return app


# POSTエンドポイントのテスト
@pytest.mark.asyncio
async def test_handle_chat_success(app):
    test_response = {'answer': 'test response'}
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(return_value=test_response)):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 201
                response_data = await response.get_json()
                assert response_data == test_response

@pytest.mark.asyncio
async def test_handle_chat_with_form(app):
    test_response = {'answer': 'test response', 'form': {'field': 'value'}}
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(return_value=test_response)):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 201
                response_data = await response.get_json()
                assert 'form' in response_data

@pytest.mark.asyncio
async def test_handle_chat_missing_user_id(app):
    async with app.test_client() as client:
        async with app.app_context():
            response = await client.post('/', json={'message': 'test'})
            assert response.status_code == 400

@pytest.mark.asyncio
async def test_handle_chat_missing_message(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            response = await client.post('/', json={})
            assert response.status_code == 400

@pytest.mark.asyncio
async def test_handle_chat_rate_limit(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(side_effect=RateLimitError("Rate limit exceeded"))):
                response = await client.post('/', json={'message': 'test'})
                assert response.status_code == 429

@pytest.mark.asyncio
async def test_handle_chat_initialized_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.store_and_respond_chat',
                      AsyncMock(side_effect=InitializedError("Failed to initialize"))):
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
                      AsyncMock(side_effect=NoChatsFoundError("No chats found"))):
                response = await client.get('/?pages=999')
                assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_chat_list_initialized_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(side_effect=InitializedError("Failed to initialize"))):
                response = await client.get('/?pages=1')
                assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_chat_list_general_error(app):
    async with app.test_client() as client:
        async with app.app_context():
            g.user_id = 'test_user'
            with patch('app.chat.chat_controller.get_paginated_chats',
                      AsyncMock(side_effect=Exception("Unexpected error"))):
                response = await client.get('/?pages=1')
                assert response.status_code == 500