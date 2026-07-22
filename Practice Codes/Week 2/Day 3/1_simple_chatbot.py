from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------- STATE ---------------- #

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---------------- NODE ---------------- #

def chat_node(state: ChatState):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


# ---------------- GRAPH ---------------- #


checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

workflow = graph.compile(checkpointer=checkpointer)


# ---------------- CHAT LOOP ---------------- #


print("Type 'exit' to quit.\n")

thread_id = '1' # thread means one interaction with the chatbot

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break


    config = {
        'configurable': {
            'thread_id': thread_id
        }
    }

    state = workflow.invoke(
        {
            "messages": [HumanMessage(content=query)]
        },

        config=config
    )

    print(f"\nAI: {state['messages'][-1].content}\n")