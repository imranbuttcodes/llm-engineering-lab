"""
1. Static Parallel Execution (Without Send)
If you always have fixed parallel tasks (e.g., always run Node B and Node C after Node A), you don't need Send. You just define normal graph edges:

Python
builder.add_edge("node_a", "node_b")
builder.add_edge("node_a", "node_c")

# Both node_b and node_c will execute in parallel automatically


2. Dynamic Parallel Execution (With Send)
Use Send when you don't know in advance how many parallel tasks there will be.

Example: An LLM generates a list of 5 sub-queries to search. You iterate through that list and return a Send object for each item.

LangGraph will launch 5 parallel instances of your search node, passing each instance its specific sub-query.



"""


import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

# 1. Define Graph State
class OverallState(TypedDict):
    topic: str
    subtopics: list[str]
    # operator.add ensures results from parallel runs are combined (fanned-in)
    results: Annotated[list[str], operator.add]

class WorkerState(TypedDict):
    subtopic: str

# 2. Define Nodes
def generate_subtopics(state: OverallState):
    # Imagine an LLM generates subtopics here
    return {"subtopics": ["LLM Architecture", "Prompt Engineering", "RAG Systems"]}

def search_subtopic(state: WorkerState):
    # This node runs in parallel for each subtopic
    subtopic = state["subtopic"]
    return {"results": [f"Search results for: {subtopic}"]}

# 3. Fan-out Conditional Routing Function
def continue_to_search(state: OverallState):
    # Dynamic Fan-Out using Send
    return [
        Send("search_subtopic", {"subtopic": s}) 
        for s in state["subtopics"]
    ]

# 4. Build the Graph
builder = StateGraph(OverallState)
builder.add_node("generate_subtopics", generate_subtopics)
builder.add_node("search_subtopic", search_subtopic)

builder.add_edge(START, "generate_subtopics")

# Add conditional edge that fans out to search_subtopic via Send
builder.add_conditional_edges(
    "generate_subtopics", 
    continue_to_search, 
    ["search_subtopic"]
)

builder.add_edge("search_subtopic", END)
graph = builder.compile()