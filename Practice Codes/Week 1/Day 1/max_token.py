import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

prompt = "Explain how airplanes fly, in detail, covering lift, thrust, drag, and weight."

print("=== max_tokens = 20 (very low, should cut off mid-sentence) ===")
llm_short = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=20,
)
response = llm_short.invoke([HumanMessage(content=prompt)])
print(response.content)
print(f"\n[Finish reason: {response.response_metadata.get('finish_reason')}]")

print()
print()
print("=== max_tokens = 300 (should complete naturally) ===")
llm_long = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=300,
)
response2 = llm_long.invoke([HumanMessage(content=prompt)])
print(response2.content)
print(f"\n[Finish reason: {response2.response_metadata.get('finish_reason')}]")