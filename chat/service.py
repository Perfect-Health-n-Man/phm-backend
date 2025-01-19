from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from chat.normal.factory import ChatFactory
from chat.normal.model import AIans

async def chat(history: FirestoreChatMessageHistory, user_message: str) -> str:
    history.add_message(HumanMessage(content=user_message))
    normal_chat = ChatFactory(history)
    result = await normal_chat.create_ans()
    result_dict = result.model_dump()
    content = result_dict.get("summary")
    history.add_messages([AIMessage(content=content)])
    return content