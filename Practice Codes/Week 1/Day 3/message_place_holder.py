from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    groq_api_key = os.getenv("GROQ_API_KEY")
)


chat_template = ChatPromptTemplate(
    [
        ('system', 'Bro You are a helpful AI assistent in domain: {domain}'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{query}')
    ]
)

chat_history = []

with open('chat_history.txt') as f:
    chat_history.extend(f.readline())


prompt = chat_template.invoke({
    'query' : 'Where is my Sh*ti refund?',
    'chat_history': chat_history,
    'domain': 'Customer Support Agent'
})



result = model.invoke(prompt)

print(result.content)