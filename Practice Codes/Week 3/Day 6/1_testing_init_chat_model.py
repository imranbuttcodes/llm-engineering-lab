from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()


# llm = init_chat_model('groq:llama-3.3-70b-versatile', configurable_fields='any')

llm = init_chat_model('llama-3.3-70b-versatile', model_provider='groq', configurable_fields='any')

print(type(llm))

print(llm.invoke('What is AI?').content)
