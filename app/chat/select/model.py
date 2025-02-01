from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class SelectAgent(BaseModel):
    cot: str = Field(description="COT thought process")
    agent_number: int = Field(description="Selected Agent Number")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0,
    max_output_tokens=1, #数字のみの出力のため
    timeout=None,
    max_retries=2,
)