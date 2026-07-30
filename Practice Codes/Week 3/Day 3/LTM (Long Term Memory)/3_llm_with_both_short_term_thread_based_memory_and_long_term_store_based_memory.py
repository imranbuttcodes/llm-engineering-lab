import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# ------------------------------------------------------------------
# 1) LONG-TERM STORE: Global memory across all threads/sessions
# ------------------------------------------------------------------
store = InMemoryStore()

# Seed long-term facts for user 'u1'
user_details_ns = ("user", "u1", "details")
store.put(user_details_ns, "profile_1", {"data": "Name: Imran Butt"})
store.put(user_details_ns, "preference_1", {"data": "Prefers concise Python examples"})

# ------------------------------------------------------------------
# 2) SHORT-TERM CHECKPOINTER: Manages conversation message history
# ------------------------------------------------------------------
checkpointer = MemorySaver()

# ------------------------------------------------------------------
# 3) GRAPH DEFINITION
# ------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """You are a helpful assistant.
User Context:
{user_details_content}

Address the user by name and keep preferences in mind.
"""

def chat_node(state: MessagesState, config: RunnableConfig, store: BaseStore):
    # Retrieve user_id from runtime config
    user_id = config["configurable"]["user_id"]

    # Retrieve Long-Term Memory (BaseStore)
    user_details_ns = ("user", user_id, "details")
    items = store.search(user_details_ns)
    user_details_content = "\n".join(f"- {it.value.get('data', '')}" for it in items)

    # Format System Message
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        user_details_content=user_details_content
    )
    system_msg = SystemMessage(content=system_prompt)

    # state["messages"] automatically contains thread history (via Checkpointer)
    response = llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

# Build state graph
builder = StateGraph(MessagesState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# Compile with BOTH store and checkpointer
graph = builder.compile(store=store, checkpointer=checkpointer)

# ------------------------------------------------------------------
# 4) RUNNING THREAD 1 (Session A)
# ------------------------------------------------------------------
config_thread_1 = {
    "configurable": {
        "user_id": "u1",        # Scopes Long-Term Memory
        "thread_id": "session_1" # Scopes Short-Term Memory
    }
}

print("--- Thread 1: Turn 1 ---")
res1 = graph.invoke(
    {"messages": [{"role": "user", "content": "Hi, I'm working on a C++ project."}]},
    config_thread_1,
)
print("AI:", res1["messages"][-1].content)

print("\n--- Thread 1: Turn 2 ---")
# Because thread_id="session_1", state retain "I'm working on a C++ project"
res2 = graph.invoke(
    {"messages": [{"role": "user", "content": "What language did I say I was using?"}]},
    config_thread_1,
)
print("AI:", res2["messages"][-1].content)

# ------------------------------------------------------------------
# 5) RUNNING THREAD 2 (Session B - New Chat)
# ------------------------------------------------------------------
config_thread_2 = {
    "configurable": {
        "user_id": "u1",        # SAME user (gets same LTM)
        "thread_id": "session_2" # NEW thread (fresh chat history)
    }
}

print("\n--- Thread 2: Turn 1 (Fresh Session) ---")
# The AI forgets the C++ comment from session_1, but STILL knows Imran and Python!
res3 = graph.invoke(
    {"messages": [{"role": "user", "content": "What language did I say I was using?"}]},
    config_thread_2,
)
print("AI:", res3["messages"][-1].content)