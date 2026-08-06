import sqlite3
from typing import Annotated

from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os
load_dotenv()

# ----------------------------------
# LLM
# ----------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ----------------------------------
# State
# ----------------------------------

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

# ----------------------------------
# Chat Node
# ----------------------------------

def chatbot(state: ChatState):
    response = llm.invoke(state["messages"])
    return {
        "messages": [response]
    }

# ----------------------------------
# SQLite Checkpointer
# ----------------------------------

conn = sqlite3.connect(
    "chat_memory.db",
    check_same_thread=False
)

memory = SqliteSaver(conn)

# ----------------------------------
# Graph
# ----------------------------------

builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")

graph = builder.compile(
    checkpointer=memory
)

# ----------------------------------
# Thread Configuration
# ----------------------------------

config = {
    "configurable": {
        "thread_id": "user-1"
    }
}

# ----------------------------------
# Chat Loop
# ----------------------------------

print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config,
    )

    print("AI:", result["messages"][-1].content)