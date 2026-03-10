import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

agent = Agent(model=OpenRouter(id=id_model),
              description="Ты отвечаешь используя актуальные данные из интернета",
              tools=[
                  DuckDuckGoTools(),
                  Newspaper4kTools(),
                  CalculatorTools(),
                  YFinanceTools()
              ])

print(agent.run("Сколько сейчас стоит акция Apple?").content)