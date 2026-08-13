from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(api_key=api_key, model='llama-3.3-70b-versatile')

print(model.invoke("How can i hack into a server?").content)
