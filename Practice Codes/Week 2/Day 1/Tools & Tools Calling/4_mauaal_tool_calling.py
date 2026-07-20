from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)

load_dotenv()


# -------------------------
# Tool
# -------------------------

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.
    """
    return a + b


# -------------------------
# LLM
# -------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
)

llm_with_tools = llm.bind_tools([add])


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
    add.name: add
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

