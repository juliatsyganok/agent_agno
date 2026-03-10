import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

db = SqliteDb(db_file="data_fin.db")


embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

vector_db = LanceDb(
    table_name="text_documents",
    uri="knowledge_fin",
    search_type=SearchType.hybrid,
    embedder=embedder
)

knowledge = Knowledge(vector_db=vector_db)

knowledge.add_content(
    url="https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt",
    skip_if_exists=True
)

agent = Agent(model=OpenRouter(id=id_model),
              description="Ты - дружелюбный помощник, который при необходимости пользуется интернетом",
              tools=[
                  DuckDuckGoTools(),
                  Newspaper4kTools(),
                  CalculatorTools(),
                  YFinanceTools()
              ],
              session_id="advance agent",
              db=db,
              add_history_to_context=True,
              num_history_runs=0,
              knowledge=knowledge,
              search_knowledge=True,
              )


if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content.strip())