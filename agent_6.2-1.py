import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

vector_db = LanceDb(
    table_name="text_documents",
    uri="lancedb_storage",
    search_type=SearchType.hybrid,
    embedder=embedder
)

knowledge = Knowledge(vector_db=vector_db)

knowledge.add_content(
    path="history.txt",
    skip_if_exists=True
)

agent = Agent(
    model=OpenRouter(id=id_model),
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True
)


if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content)