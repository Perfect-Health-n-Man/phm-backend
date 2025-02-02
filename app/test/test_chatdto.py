from app.chat.chat_dto import ChatDto


def test_response_model():
    response = ChatDto(answer="ai_answer", form=["a", "b", "c"])
    response_str = response.to_str()
    assert response_str == """answer: ai_answer

1. a
2. b
3. c"""