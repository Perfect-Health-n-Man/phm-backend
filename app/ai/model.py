from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.callback import CallbackHandler

def get_llm_model_and_callback(session_id: str) -> tuple[ChatGoogleGenerativeAI, CallbackHandler]:
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0,
        max_output_tokens=1000,
        timeout=None,
        max_retries=2,
    ), CallbackHandler(session_id=session_id)

