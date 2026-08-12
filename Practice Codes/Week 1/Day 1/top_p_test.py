import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

prompt = "Write a short, imaginative opening line for a fantasy novel."

print("=== High temp (1.3) + top_p = 1.0 (no restriction) ===")
llm_wide = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=1.3,
    model_kwargs={"top_p": 1.0},
)
for i in range(3):
    response = llm_wide.invoke([HumanMessage(content=prompt)])
    print(f"[{i+1}] {response.content}")

print()
print("=== High temp (1.3) + top_p = 0.1 (very restrictive) ===")
llm_narrow = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=1.3,
    model_kwargs={"top_p": 0.1},
)
for i in range(3):
    response = llm_narrow.invoke([HumanMessage(content=prompt)])
    print(f"[{i+1}] {response.content}")