from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import base64
import os 
from dotenv import load_dotenv

load_dotenv()

# Encode image to base64
with open("PipeLine MindMap.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

# Point to OpenRouter's dynamic free router
llm = ChatOpenAI(
    model="openrouter/free",  # Automatically selects an available free vision model
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url="https://openrouter.ai/api/v1",
)

message = HumanMessage(
    content=[
        {"type": "text", "text": "Extract all text and summarize this diagram:"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
    ]
)

response = llm.invoke([message])
print(response.content)