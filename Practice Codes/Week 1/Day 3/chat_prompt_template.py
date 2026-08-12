# Dynamic Set of Messages 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, load_prompt
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq


load_dotenv()

model = ChatGroq(model = 'llama-3.3-70b-versatile',
                 temperature=2,
                 groq_api_key = os.getenv("GROQ_API_KEY"))


#prompt_template = load_prompt('prompt_template.json')
chat_template = ChatPromptTemplate.from_messages(
    [
        ('system','You are an AI Assistent expert in {domain}'),
        ('human','Explain in Simple Terms in one line What is {topic}')
    ]
)

prompt = chat_template.invoke({
    'domain': "Computer Science",
    'topic': 'Recursion'
})

print(prompt)
print()

response = model.invoke(prompt)

print(response.content)

# promptTemplate is used in single-turn conversations while ChatPromptTemplate is used in multi-turn conversations. 