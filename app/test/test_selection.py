from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.select.factory import SelectAgentFactory
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()

from app.chat.chat_repository import get_chat_history


@pytest.mark.asyncio(loop_scope="session")
async def test_select_agent():
    user_info, task = await get_user_info_and_tasks("WH3FePgXPScZGKoJ0qIQ")
    state = State(
        user_message="ニックネームを変更したい",
        history=get_chat_history("WH3FePgXPScZGKoJ0qIQ").to_history_str(),
        datetimeNow=datetime.now().isoformat(),
        tasks=task,
        user_info=user_info,
        session_id="test_selection"
    )
    selection = SelectAgentFactory(session_id="test_selection")
    result = await selection.create_ans(state)
    agent = result.get("current_agent")
    assert type(agent) is int
    assert agent == 2
    print("agent", agent)
