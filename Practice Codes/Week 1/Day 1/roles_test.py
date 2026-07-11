import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

response_plain = llm.invoke([
    HumanMessage(content="What's 15 * 12?")
])
print("=== No system role ===")
print(response_plain.content)
print()

response_shaped = llm.invoke([
    SystemMessage(content="You are a strict math tutor. NEVER give the final answer directly. Only give a hint that helps the student figure it out themselves."),
    HumanMessage(content="What's 15 * 12?")
])
print("=== With system role (strict tutor) ===")
print(response_shaped.content)