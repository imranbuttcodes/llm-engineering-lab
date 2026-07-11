import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

prompt = "Write a short motivational line for a student learning AI."

print("=== Temperature = 0 (should look nearly identical each time) ===")
llm_cold = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)
for i in range(3):
    response = llm_cold.invoke([HumanMessage(content=prompt)])
    print(f"[{i+1}] {response.content}")

print()
print("=== Temperature = 1.5 (should vary noticeably each time) ===")
llm_hot = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=1.5,
)
for i in range(3):
    response = llm_hot.invoke([HumanMessage(content=prompt)])
    print(f"[{i+1}] {response.content}")