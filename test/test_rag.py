from dotenv import load_dotenv
load_dotenv()

from langchain_google_community import VertexAISearchRetriever
from chat.rag.factory import RagFactory

def test_rag():
    rag = RagFactory()
    assert type(rag.retriever) is VertexAISearchRetriever