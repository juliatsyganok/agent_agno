import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

agent = Agent(model=OpenRouter(id=id_model))

if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content)