from langchain_core.messages import (
    HumanMessage, ToolMessage
)

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """
    This Function Adds two integers and return the result
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """
    This Function multiply two integers and return the result
    """
    return a * b


@tool
def divide(a: int, b: int) -> int:
    """
    This Function divides two integers and return the result
    """
    if b == 0:
        b = 1
    return a / b

@tool
def subtract(a: int, b: int) -> int:
    """
    This Function subtract two integers and return the result
    """
    return a - b



llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    api_key=os.getenv('GROQ_API_KEY')
)

available_tools = {
    add.name: add,
    multiply.name: multiply,
    subtract.name: subtract,
    divide.name: divide
}

llm_with_tools = llm.bind_tools([add, multiply, subtract, divide])



while True:
    query = input('Calculate Anything: ')

    if query == 'exit':
        break
    
    user_message = HumanMessage(
        content=query
    )

    response = llm_with_tools.invoke(
        [
            user_message
        ]
    )

    print("LLM RESPONSE")
    print()
    print(response)
    print()
    print()
    
    if response.tool_calls:

        tool_messeges = []

        for tool_call in response.tool_calls:
            print('='*60)
            print('Tool Call')
            print(tool_call)
            print('=' * 60)

            selected_tool = available_tools[
                tool_call['name']
            ]

            tool_result = selected_tool.invoke(
                tool_call['args']
            )

            print("TOOL RESULt:", tool_result)

            tool_messeges.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id = tool_call['id']
                )
            )

        result = llm_with_tools.invoke(
            [
                user_message,
                response,
                *tool_messeges # That * unpacks all the ToolMessage objects.
            ]
        )
        print("FINAL ANSEWR")
        print()
        print(result.content)
    else:
        print("FINAL ANSEWR")
        print()
        print(response.content)