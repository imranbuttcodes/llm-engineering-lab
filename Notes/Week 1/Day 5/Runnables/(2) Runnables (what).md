LET'S GOOOO! 🔥🚀

Welcome to **Day 5: Runnables**.

This topic is one of the **core pillars of LangChain**. Once you master Runnables, almost every advanced feature—**RAG, Agents, LangGraph, MCP, Multi-Agent Systems**—will feel much easier because they're all built on top of the Runnable interface.

# Today's Roadmap

```text
Runnables
│
├── Why Runnables? ✅
│
├── What is a Runnable?
│
├── Runnable Interface
│   ├── invoke()
│   ├── batch()
│   ├── stream()
│   ├── ainvoke()
│   ├── abatch()
│   └── astream()
│
├── RunnableLambda
│
├── RunnablePassthrough
│
├── RunnableAssign
│
├── RunnablePick
│
├── RunnableMap (if applicable)
│
├── RunnableSequence
│
├── RunnableParallel (Revision)
│
├── RunnableBranch (Revision)
│
└── Mini Projects
```

---

# What is a Runnable?

A **Runnable** is simply an object that **can perform some task**.

That's it.

In LangChain, if an object follows the Runnable interface, it knows how to accept an input, process it, and produce an output.

You can think of it like a function.

```
Input
  │
  ▼
Runnable
  │
  ▼
Output
```

For example,

```
Input:
"What is AI?"

↓

Chat Model

↓

"Artificial Intelligence is..."
```

or

```
Input:
{"topic":"Python"}

↓

PromptTemplate

↓

"Explain Python..."
```

Both are completely different objects...

...but both are **Runnables**.

---

# The Runnable Contract

Every Runnable promises:

> "Give me an input, and I'll give you an output."

This contract allows LangChain to chain everything together.

```
Prompt
   │
   ▼
Model
   │
   ▼
Parser
```

Each block doesn't need to know how the next one works.

It only knows:

> "I'm passing my output to another Runnable."

---

# Every Runnable Supports the Same Methods

This is the most important thing to remember.

Every Runnable supports methods like:

| Method      | Purpose                                        |
| ----------- | ---------------------------------------------- |
| `invoke()`  | Process one input                              |
| `batch()`   | Process multiple inputs                        |
| `stream()`  | Return output token-by-token or chunk-by-chunk |
| `ainvoke()` | Async version of invoke                        |
| `abatch()`  | Async version of batch                         |
| `astream()` | Async streaming                                |

This consistency is what makes LangChain so composable.

---

# Example 1: PromptTemplate is a Runnable

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic}"
)

result = prompt.invoke({
    "topic": "Machine Learning"
})

print(result)
```

Input:

```
Machine Learning
```

↓

Output:

```
Explain Machine Learning
```

No LLM involved.

Still a Runnable.

---

# Example 2: Chat Model is a Runnable

```python
response = model.invoke(
    "What is AI?"
)
```

Input

```
Question
```

↓

Output

```
AI Answer
```

Again...

Runnable.

---

# Example 3: Output Parser is a Runnable

```python
parser = StrOutputParser()

result = parser.invoke(response)
```

Input

```
AIMessage
```

↓

Output

```
String
```

Again...

Runnable.

---

# Why This Is Powerful

Since every component is a Runnable...

they can all be connected.

```python
chain = prompt | model | parser
```

The `|` operator works because each object follows the same interface.

---

# Runnable Flow

```
User Input
     │
     ▼
PromptTemplate
     │
     ▼
Chat Model
     │
     ▼
Output Parser
     │
     ▼
Final Result
```

Notice that every box is just another Runnable.

---

# Think of Runnables Like Workers

Imagine a company.

```
Customer

↓

Receptionist

↓

Engineer

↓

Quality Checker

↓

Delivery
```

Each employee has a different job.

But they all follow the same workflow:

* Receive work
* Do work
* Pass work forward

That's exactly how Runnables operate.

---

# Runnables Are Everywhere

You've already been using them for the past few days without realizing it!

```python
prompt
```

✔ Runnable

```python
ChatGroq
```

✔ Runnable

```python
ChatHuggingFace
```

✔ Runnable

```python
StrOutputParser
```

✔ Runnable

```python
JsonOutputParser
```

✔ Runnable

```python
PydanticOutputParser
```

✔ Runnable

```python
RunnableParallel
```

✔ Runnable

```python
RunnableBranch
```

✔ Runnable

Even your **entire chain** is itself a Runnable!

```python
chain = prompt | model | parser

chain.invoke(...)
chain.batch(...)
chain.stream(...)
```

A chain can be nested inside another chain because it follows the same Runnable interface.

---

# Key Takeaways

* A **Runnable** is any object that follows LangChain's standard processing interface.
* Every Runnable takes an input, performs some work, and returns an output.
* Common Runnable methods include `invoke()`, `batch()`, `stream()`, and their asynchronous counterparts.
* Prompts, chat models, output parsers, and even complete chains are all Runnables.
* Because they all share the same interface, they can be combined seamlessly using the `|` operator to build complex AI workflows.

---

## 🚀 Next Topic

Now that you know **what a Runnable is**, the next logical step is to learn the methods every Runnable provides.

We'll start with the most important one:

> **`invoke()`** (a quick revision with deeper understanding), then move to **`batch()`**, **`stream()`**, **`ainvoke()`**, and finally the specialized Runnable classes like **`RunnableLambda`**, **`RunnablePassthrough`**, and **`RunnableAssign`**.
