Let's go! 🔥

This is one of the biggest transitions in LLM engineering.

Until now, your LLM has been like a **very knowledgeable human sitting in a room**. It can only answer from:

* its training data
* your prompt
* RAG context

It **cannot interact with the outside world**.

A Tool changes that.

---

# Day 8 — Tool Calling

## Chapter 1 — What is a Tool?

Imagine asking ChatGPT:

> **"What's the weather in Lahore?"**

Without tools, the LLM can only guess.

With tools:

```
User
   │
   ▼
LLM
   │
"I need weather."
   │
   ▼
Weather Tool
   │
Returns JSON
   │
   ▼
LLM
   │
Formats answer
   ▼
User
```

The LLM doesn't magically know the weather.

It **knows WHEN to use a tool**.

---

## Another Example

User:

> What's 923489 × 23423?

Instead of trying to multiply mentally...

```
LLM
   │
Need calculator
   ▼
Calculator Tool
   │
216337...
   ▼
LLM
```

---

## Think of a Tool as...

A normal Python function.

Nothing more.

Example:

```python
def add(a, b):
    return a + b
```

That's just Python.

To make it available to an LLM...

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int):
    """Add two integers."""
    return a + b
```

Congratulations.

That function is now a Tool.

---

# Why the Docstring?

The LLM reads it.

Example

```python
@tool
def weather(city):
    """
    Get current weather of a city.
    """
```

The model literally sees:

> There is a tool named **weather**.

> It gets the current weather.

So if someone asks

> Weather in Paris?

it knows exactly what to call.

---

# Why Type Hints?

```python
def add(
    a: int,
    b: int
)
```

The LLM also reads these.

It understands

```
Needs integer

Needs integer
```

instead of

```
Anything?
```

---

# Under the hood

When you write

```python
@tool
def multiply(a: int, b: int):
    """Multiply two numbers."""
```

LangChain converts it into something like

```json
{
  "name": "multiply",
  "description": "Multiply two numbers.",
  "parameters": {
    "a": "integer",
    "b": "integer"
  }
}
```

This schema is sent to the LLM.

The LLM decides

> I should call multiply.

---

# Important Concept

The LLM **does NOT execute** your Python function.

It only says:

```
Call:

multiply(
    a=5,
    b=10
)
```

Your Python code executes it.

---

# Think of it like this

```
LLM
│
│
"I need calculator"
│
▼
Python
│
│
Runs calculator()
│
▼
Returns result
│
▼
LLM
│
▼
Final answer
```

The LLM is the **decision maker**.

Python is the **worker**.

---

# Types of Tools you'll build

We'll start simple.

### 1. Calculator

```
Add

Subtract

Multiply

Divide
```

---

### 2. Time Tool

```
Current Time
```

---

### 3. Weather Tool

(API later)

---

### 4. Wikipedia Tool

---

### 5. File Reader

---

### 6. SQL Tool

---

### 7. RAG Tool

Your PDF chatbot can become a tool.

---

### 8. Web Search Tool

---

# Today's Goal

By the end of today, you'll understand:

* ✅ What a Tool is
* ✅ `@tool`
* ✅ Tool schema
* ✅ Why docstrings matter
* ✅ Why type hints matter
* ✅ How the LLM decides to use a tool
* ✅ How tool execution works

---

## 🚀 First Practical Exercise

Create a new file:

```
Day-8/
│
├── tools_demo.py
```

Write exactly this:

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.
    """
    return a + b


print(add)

print(type(add))
```

Run it and show me the output.

From there, we'll inspect what `@tool` actually does under the hood before we move on to binding tools to an LLM. This step will make the rest of tool calling much easier to understand.
