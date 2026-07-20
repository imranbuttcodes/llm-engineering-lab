from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from dotenv import load_dotenv
import os


load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """
    This Function Returns addition of two numbers
    
    """

    return a + b


tools = {
    add.name: add
}

llm = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))


# Now bind_tool internally does llm + tools and returns new RUNNABLE
new_llm = llm.bind_tools([add])

# print(type(llm))
# print(type(new_llm))
# print(new_llm)

response = new_llm.invoke('What is 2 + 2 = ')


# print(response.tool_calls)



tool_call = response.tool_calls[0]

selected_tool = tools[
    tool_call['name']
]

result = selected_tool.invoke(
    tool_call['args']
)

print("Result:",result)

print(add)
print(add.name)