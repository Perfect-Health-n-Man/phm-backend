from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.select.factory import SelectAgentFactory

load_dotenv()

from app.chat.chat_repository import get_chat_history

state = State(
    user_message="ニックネームを変更したい",
    history=get_chat_history("WH3FePgXPScZGKoJ0qIQ").to_history_str(),
    datetimeNow=datetime.now().isoformat(),
)

@pytest.mark.asyncio
async def test_select_agent():
    selection = SelectAgentFactory()
    result = await selection.create_ans(state)
    agent = result.get("current_agent")
    assert type(agent) is int
    assert agent == 2
    print("agent", agent)
