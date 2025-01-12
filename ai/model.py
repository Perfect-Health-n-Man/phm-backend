from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.callback import CallbackHandler

langfuse_callback_handler = CallbackHandler()

def get_llm_model_and_callback():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    ), langfuse_callback_handler