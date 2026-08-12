from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import load_prompt
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model = 'llama-3.3-70b-versatile', top_p = 0.9)


#template = load_prompt('prompt_template.json')

message  =[
    HumanMessage(content = "IMRAN BUTT is GOAT"),
    SystemMessage(content = 'You are a top class CS Teacher and motivate students in their CS and Personal Life'),
]

result = model.invoke(message)

message.append(AIMessage(content=result.content))
print(result.content)
print()
print()
print(message)
