# 📘 LangGraph Streaming

Streaming in **LangGraph** allows you to receive updates **while a graph is executing**, instead of waiting for the entire workflow to finish.

Without streaming, the graph executes all nodes and returns only the final result. With streaming, you can observe the workflow in real time.

---

# Why Streaming?

Consider the following workflow:

```text
Search Database
        │
        ▼
Read PDF
        │
        ▼
Call LLM
        │
        ▼
Generate Answer
```

If each node takes 5 seconds, using `invoke()` the user waits **20 seconds** before seeing anything.

With streaming:

```text
🔍 Searching Database...
✅ Done

📄 Reading PDF...
✅ Done

🤖 Calling LLM...
✅ Done

📝 Generating Answer...
```

The user can see the workflow progressing in real time.

---

# invoke() vs stream()

## invoke()

Runs the complete graph and returns only the final state.

```python
result = workflow.invoke(initial_state)

print(result)
```

Execution:

```text
Node 1
↓

Node 2
↓

Node 3
↓

Return Final State
```

---

## stream()

Runs the graph while yielding intermediate updates.

```python
for event in workflow.stream(initial_state):
    print(event)
```

Execution:

```text
Node 1
↓

Update

↓

Node 2

↓

Update

↓

Node 3

↓

Update
```

---

# Simple Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str

def node1(state):
    state["text"] += " -> Node1"
    return state

def node2(state):
    state["text"] += " -> Node2"
    return state

builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)

workflow = builder.compile()
```

Using `invoke()`:

```python
workflow.invoke({"text": "Start"})
```

Output

```text
{
    'text': 'Start -> Node1 -> Node2'
}
```

---

Using `stream()`:

```python
for event in workflow.stream(
    {"text": "Start"},
    stream_mode="updates"
):
    print(event)
```

Output

```text
{
    'node1': {
        'text': 'Start -> Node1'
    }
}

{
    'node2': {
        'text': 'Start -> Node1 -> Node2'
    }
}
```

---

# Stream Modes

LangGraph supports multiple stream modes.

---

## 1. updates ⭐⭐⭐⭐⭐

Streams **only the output returned by each node**.

```python
for event in workflow.stream(
    initial_state,
    stream_mode="updates"
):
    print(event)
```

Example

```text
{
    'generate_summary': {
        'summary': '...'
    }
}

{
    'translate': {
        'translation': '...'
    }
}
```

Best for:

* Agent workflows
* Monitoring node execution
* Production applications

---

## 2. values ⭐⭐☆☆☆

Streams the **entire graph state** after every node.

```python
for event in workflow.stream(
    initial_state,
    stream_mode="values"
):
    print(event)
```

Example

```text
{
    'topic': 'AI'
}

{
    'topic': 'AI',
    'summary': '...'
}

{
    'topic': 'AI',
    'summary': '...',
    'translation': '...'
}
```

Useful for:

* Debugging
* Learning
* Inspecting state evolution

---

## 3. messages ⭐⭐⭐⭐⭐

Streams **LLM tokens** as they are generated.

Enable streaming:

```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    streaming=True
)
```

Then:

```python
for token, metadata in workflow.stream(
    initial_state,
    stream_mode="messages"
):
    print(token.content, end="")
```

Output

```text
Artificial
 Intelligence
 is
 transforming
 the
 world...
```

Exactly like ChatGPT typing.

Best for:

* Chatbots
* Streaming UI
* Real-time responses

---

## 4. debug ⭐☆☆☆☆

Streams debugging information.

```python
for event in workflow.stream(
    initial_state,
    stream_mode="debug"
):
    print(event)
```

Example

```text
Running node generate_summary

State Updated

Running node translate

State Updated

Graph Finished
```

Mostly used while debugging graphs.

---

## 5. custom ⭐⭐⭐⭐☆

Allows developers to stream **their own custom events**.

Inside a node:

```python
from langgraph.config import get_stream_writer

def process(state):

    writer = get_stream_writer()

    writer("Reading PDF...")

    ...

    writer("Finished Reading PDF")

    return {...}
```

Streaming:

```python
for event in workflow.stream(
    initial_state,
    stream_mode="custom"
):
    print(event)
```

Output

```text
Reading PDF...

Finished Reading PDF
```

Useful for:

* Progress bars
* Logging
* Streamlit status updates
* Custom UI events

---

# Which Modes Are Used Most?

| Mode     | Use Case         | Usage |
| -------- | ---------------- | ----- |
| updates  | Node outputs     | ⭐⭐⭐⭐⭐ |
| messages | Token streaming  | ⭐⭐⭐⭐⭐ |
| custom   | Progress updates | ⭐⭐⭐⭐☆ |
| values   | State inspection | ⭐⭐☆☆☆ |
| debug    | Debugging        | ⭐☆☆☆☆ |

---

# Best Practices

✅ Use **invoke()** when you only need the final result.

✅ Use **updates** for most workflow execution.

✅ Use **messages** for chatbot applications.

✅ Use **custom** for progress indicators and UI updates.

✅ Use **values** when inspecting how the state changes over time.

✅ Use **debug** only while troubleshooting.

---

# Quick Interview Answer

> **Streaming in LangGraph allows a graph to emit intermediate updates while executing instead of waiting for completion. It improves responsiveness in AI applications by streaming node outputs, LLM tokens, or custom events in real time.**
