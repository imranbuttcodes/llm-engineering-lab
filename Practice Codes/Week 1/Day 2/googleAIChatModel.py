from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite', google_api_key=api_key)

response = model.invoke('What is AI BRO ?')

print(response.text)