from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool, BaseTool
from typing import Type




load_dotenv()


# -------------------------
# Tool
# -------------------------


class AddNumbers(BaseModel):
    a: int = Field(description='First number to add')
    b: int = Field(description='Second number to add')



def add(a: int, b: int) -> int:
    """
    Add two integers.
    """
    return a + b

add_tool = StructuredTool.from_function(
    description='This Function Adds Two Integers',
    func=add,
    args_schema=AddNumbers,
    name='add'
)


class Multiply(BaseModel):
    a: int = Field(description='First number to multiply')
    b: int = Field(description='Second number to multiply')



class MultiplyTool(BaseTool):
    name: str = 'Multiply_'
    description: str = "Multiply Two Numbers"

    args_schema: Type[BaseModel] = Multiply

    def _run(self, a: int, b: int) -> int:
        return a * b

# -------------------------
# LLM
# -------------------------

multiply_tool = MultiplyTool()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
)

llm_with_tools = llm.bind_tools([add_tool, multiply_tool])


# -------------------------
# User Message
# -------------------------

query = input('Ask for addition: ')

messages = [
    HumanMessage(
        content=query
    )
]


# -------------------------
# First LLM Call
# -------------------------

response = llm_with_tools.invoke(messages)

print("=" * 70)
print("LLM Response")
print("=" * 70)
print(response)
print()


# -------------------------
# Extract Tool Call
# -------------------------

tool_call = response.tool_calls[0]

print("=" * 70)
print("Tool Call")
print("=" * 70)
print(tool_call)
print()


# -------------------------
# Execute Tool
# -------------------------

tools = {
    add_tool.name: add_tool,
    multiply_tool.name:  multiply_tool
}

selected_tool = tools[
    tool_call["name"]
]

tool_result = selected_tool.invoke(
    tool_call["args"]
)

print("=" * 70)
print("Tool Result")
print("=" * 70)
print(tool_result)
print()


# -------------------------
# Create ToolMessage
# -------------------------

tool_message = ToolMessage(
    content=str(tool_result),
    tool_call_id=tool_call["id"],
)


# -------------------------
# Final LLM Call
# -------------------------

final_response = llm_with_tools.invoke(
    [
        *messages,
        response,
        tool_message,
    ]
)

print("=" * 70)
print("Final Answer")
print("=" * 70)
print(final_response.content)
print()
print()
print(final_response)

