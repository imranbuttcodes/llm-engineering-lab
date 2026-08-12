from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    groq_api_key = api_key
)

# prompt = load_prompt('prompt_template.json')

# it is of Multi-Turn (Static Message) 
chat_history = [
    SystemMessage('You are a CS HelpFull AI assistant')
]
while True:
    user_input = input("You: ")
    chat_history.append(HumanMessage(content = user_input))
    if user_input == 'exit':
        break
    
    response = model.invoke(chat_history)
    chat_history.append(AIMessage(content = response.content))

    print("AI:",response.content)

print(chat_history)