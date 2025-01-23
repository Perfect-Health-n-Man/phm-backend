from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from datetime import datetime

from app.chat.normal.factory import ChatFactory


async def chat(history: FirestoreChatMessageHistory, user_message: str) -> str:
    history.add_message(HumanMessage(content=user_message, additional_kwargs={'datetime': datetime.now()}))
    normal_chat = ChatFactory(history)
    result = await normal_chat.create_ans()
    result_dict = result.model_dump()
    content = result_dict.get("summary")
    history.add_messages([AIMessage(content=content, additional_kwargs={'datetime': datetime.now()})])
    return content