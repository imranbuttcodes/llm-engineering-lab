import os
import requests
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EXCHANGE_API_KEY = os.getenv("CURRENCY_RATE_API_KEY")

# ----------------------------------------------------
# Tools
# ----------------------------------------------------

@tool
def get_conversion_rate(
    base_currency: str,
    target_currency: str,
) -> float:
    """
    Returns the conversion rate between two currencies.

    Example:
    USD -> PKR
    EUR -> USD
    """

    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{EXCHANGE_API_KEY}/pair/"
        f"{base_currency}/{target_currency}"
    )

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    return data["conversion_rate"]


@tool
def convert_currency(
    amount: float,
    conversion_rate: float,
) -> float:
    """
    Converts an amount using a conversion rate.
    """

    return amount * conversion_rate


# ----------------------------------------------------
# LLM
# ----------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
)

llm_with_tools = llm.bind_tools(
    [
        get_conversion_rate,
        convert_currency,
    ]
)

# ----------------------------------------------------
# Available Tools
# ----------------------------------------------------

available_tools = {
    get_conversion_rate.name: get_conversion_rate,
    convert_currency.name: convert_currency,
}

# ----------------------------------------------------
# Conversation Memory
# ----------------------------------------------------

messages = []

# ----------------------------------------------------
# Chat Loop
# ----------------------------------------------------

while True:

    query = input("\nAsk Anything: ")

    if query.lower() == "exit":
        break

    # -----------------------------
    # User Message
    # -----------------------------

    user_message = HumanMessage(content=query)

    messages.append(user_message)

    # -----------------------------
    # First LLM Call
    # -----------------------------

    response = llm_with_tools.invoke(messages)

    messages.append(response)

    # -----------------------------
    # No Tool Needed
    # -----------------------------

    if not response.tool_calls:

        print("\nAssistant:")
        print(response.content)

        continue

    # -----------------------------
    # Execute ALL Tools
    # -----------------------------

    tool_messages = []

    for tool_call in response.tool_calls:

        print("=" * 70)
        print("Tool Selected:")
        print(tool_call["name"])
        print("Arguments:")
        print(tool_call["args"])
        print("=" * 70)

        selected_tool = available_tools[
            tool_call["name"]
        ]

        tool_result = selected_tool.invoke(
            tool_call["args"]
        )

        print("Tool Result:")
        print(tool_result)

        tool_messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )
        )

    # -----------------------------
    # Append ALL Tool Messages
    # -----------------------------

    messages.extend(tool_messages)

    # -----------------------------
    # Final LLM Call
    # -----------------------------

    final_response = llm_with_tools.invoke(messages)

    messages.append(final_response)

    print("\nAssistant:")
    print(final_response.content)