from dotenv import load_dotenv
load_dotenv()

from ai.model import get_llm_model_and_callback
from ai.prompt import get_prompt
from langchain_core.output_parsers import StrOutputParser
from langfuse import Langfuse
from datetime import datetime
from google.cloud import firestore
import asyncio

async def get_user_info(db: firestore.AsyncClient, user_id: str) -> dict:
    user_ref = await db.collection("users").document(user_id).get()
    user_info = user_ref.to_dict()["user_info"]
    user_info["datetimeNow"] = datetime.now()
    return user_info

async def create_tasks(fs_client: firestore.AsyncClient, lf_client: Langfuse, user_id: str) -> str:
    langchain_prompt = get_prompt(lf_client, "createDailyTasks")
    user_info = await get_user_info(fs_client, user_id)

    model, langfuse_handler = get_llm_model_and_callback()
    output_parser = StrOutputParser()
    chain = langchain_prompt | model | output_parser
    return chain.invoke(input=user_info, config={"callbacks":[langfuse_handler]})

def get_tasks(): ...

def update_tasks(): ...

def delete_tasks(): ...

async def main():
    fs_client = firestore.AsyncClient()
    lf_client = Langfuse()
    result = await create_tasks(fs_client, lf_client, "user-id")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())