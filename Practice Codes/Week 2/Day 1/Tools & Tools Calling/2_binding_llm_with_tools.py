from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """
    This Function Returns addition of two numbers
    
    """

    return a + b


llm = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))


# Now bind_tool internally does llm + tools and returns new RUNNABLE
new_llm = llm.bind_tools([add])

# print(type(llm))
# print(type(new_llm))
# print(new_llm)

result = new_llm.invoke('What is 2 + 2 = ')
print(result)
print()
print()
result = new_llm.invoke('What is 123 + 456?')
print(result)
print()
print()
result = new_llm.invoke('Can you add 999 and 1?')
print(result)
print()
print()
result = new_llm.invoke('Please sum 88 and 12.')
print(result)
print()
print()

result = new_llm.invoke('Find the addition of 400 and 600.')
print(result)
print()
print()
