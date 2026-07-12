# This is ChatModel Not LLM

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

chatmodel = ChatOpenAI(
        model="openrouter/free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
    )



response = chatmodel.invoke([
    HumanMessage(content='what is AI in one sentence in funniest possible way!')
])

print(response.content)