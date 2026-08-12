from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

from langchain_groq import ChatGroq

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    RemoveMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3


# ==========================================
# ENV
# ==========================================

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


summerization_llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# ==========================================
# STATE
# ==========================================

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str


# ==========================================
# CHAT NODE
# ==========================================

def chatbot(state: ChatState):

    summary = state.get("summary", "")

    messages = []

    if summary:
        messages.append(
            SystemMessage(
                content=f"""
Conversation Summary:

{summary}

Use this summary as memory while answering.
"""
            )
        )

    messages.extend(state["messages"])

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }


# ==========================================
# SUMMARIZE NODE
# ==========================================

def summarize_node(state: ChatState):

    old_summary = state.get("summary", "")

    if old_summary:

        prompt = f"""
Current Summary:

{old_summary}

Extend this summary using the new conversation.

Keep:

- User information
- Preferences
- Important facts
- Previous discussions
- Long-term memory
"""

    else:

        prompt = """
Create a concise summary of this conversation.

Keep:

- User information
- Preferences
- Important facts
"""

    print()
    print(state['messages'])
    print()
    print("That was before calling llm")
    response = summerization_llm.invoke(

        [HumanMessage(content=prompt)] +

        state["messages"]

    )

    print("SUMMARY CREATED")
    print(response.content)

    delete_messages = [

        RemoveMessage(id=m.id)

        for m in state["messages"][:-2]

    ]

    return {

        "summary": response.content,

        "messages": delete_messages

    }


# ==========================================
# ROUTER
# ==========================================

def should_summarize(state: ChatState):

    if len(state["messages"]) >= 10:
        return "summarize"

    return END


# ==========================================
# GRAPH
# ==========================================

conn = sqlite3.connect(database='summerization_stm3.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)



builder = StateGraph(ChatState)

builder.add_node("chat", chatbot)

builder.add_node("summarize", summarize_node)

builder.add_edge(START, "chat")

builder.add_conditional_edges(
    "chat",
    should_summarize
)

builder.add_edge(
    "summarize",
    END
)

graph = builder.compile(
    checkpointer=checkpointer
)


# ==========================================
# CONFIG
# ==========================================

config = {

    "configurable": {

        "thread_id": "thread_1"

    }

}


# ==========================================
# CLI LOOP
# ==========================================

print("=" * 60)
print(" LangGraph Summarization Memory Chatbot ")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    user = input("\nYou : ")

    if user.lower() == "exit":
        break

    result = graph.invoke(

        {

            "messages": [

                HumanMessage(content=user)

            ]

        },

        config=config

    )

    print("\nAI :", result["messages"][-1].content)

    state = graph.get_state(config)

    print("DEBUG:", repr(state.values))

    print("\n----------------------------")
    print("Stored Messages :", len(state.values["messages"]))

    # print(state)    
    summary = state.values.get("summary")   

    if summary:

        print("\nCurrent Summary\n")

        print(summary)

    else:

        print("\nNo Summary Yet")

    print("----------------------------")