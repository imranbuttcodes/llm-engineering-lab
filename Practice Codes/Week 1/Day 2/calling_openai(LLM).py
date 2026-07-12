# This is LLM Not ChatModel
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

llm = OpenAI(model='openrouter/free', 
             openai_api_key=api_key,
               openai_api_base="https://openrouter.ai/api/v1"
               )

response = llm.invoke("What is the capital of Pakistan")

print(response)