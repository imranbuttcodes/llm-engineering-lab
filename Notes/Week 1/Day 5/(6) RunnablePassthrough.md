LET'S GOOOO!! 🔥🔥

Now we're entering one of the most useful Runnable primitives. These three are closely related, so by the end you'll understand exactly **when to use each one**.

---

# Today's Roadmap

```text
Runnable Data Manipulation
│
├── RunnablePassthrough
│   ├── Why?
│   ├── Basic Example
│   ├── Chain Example
│   ├── Real-World Example
│   └── Why RAG uses it
│
├── RunnableAssign
│   ├── Why?
│   ├── Add New Keys
│   ├── Parallel Example
│   ├── LLM Example
│   └── Real-World Example
│
└── RunnablePick
    ├── Why?
    ├── Select Keys
    ├── Chain Example
    └── Real-World Example
```

---

# Part 1 — RunnablePassthrough

## Why do we need it?

Imagine you have a pipeline.

```text
Question
   │
   ▼
LLM
```

Everything works.

But suppose later you also need the **original question**.

For example

```
Question:
"What is AI?"
```

↓

LLM

↓

```
"Artificial Intelligence is..."
```

Oops...

The original question disappeared.

Sometimes we want BOTH.

```
Question
```

AND

```
Answer
```

How?

That's exactly why `RunnablePassthrough` exists.

---

# Definition

> **RunnablePassthrough simply returns whatever it receives without changing it.**

It is literally an identity function.

Mathematically,

```
f(x)=x
```

---

# Visual

```
Input
 │
 ▼
RunnablePassthrough
 │
 ▼
Same Input
```

---

# Example 1

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

print(
    passthrough.invoke("Hello")
)
```

Output

```
Hello
```

Nothing happened.

---

Example 2

```python
print(
    passthrough.invoke(25)
)
```

Output

```
25
```

---

Example 3

```python
print(
    passthrough.invoke(
        {
            "name":"Imran",
            "age":21
        }
    )
)
```

Output

```python
{
    "name":"Imran",
    "age":21
}
```

Exactly the same dictionary.

---

# Isn't this useless? 🤔

At first glance...

YES 😂

Most people think

> "Bro... why create a Runnable that literally does nothing?"

The answer comes when building chains.

---

# Example with RunnableParallel

Suppose you have

```
Question

↓

LLM

↓

Answer
```

But you also want to preserve the original question.

You can split the flow.

```text
                 Question
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
Passthrough                  LLM
          │                     │
          ▼                     ▼
Original Question          Generated Answer
```

Code

```python
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough

chain = RunnableParallel({

    "question": RunnablePassthrough(),

    "answer": prompt | model | parser

})
```

Input

```python
{
    "topic":"Python"
}
```

Output

```python
{
    "question":{
        "topic":"Python"
    },

    "answer":"Python is..."
}
```

Notice

The same input goes to BOTH branches.

---

# Why not duplicate manually?

You could...

```python
question = user_input

answer = model.invoke(question)

result = {

    "question":question,

    "answer":answer

}
```

RunnablePassthrough lets LCEL do it automatically.

---

# Real Example

Suppose you build ChatGPT.

User asks

```
What is PCA?
```

The LLM generates

```
PCA stands for Principal Component Analysis...
```

Later,

you want to save

```python
{
    "question": "...",
    "answer":"..."
}
```

RunnablePassthrough preserves the original question.

---

# RAG Example

This is where it becomes SUPER useful.

```
Question
      │
      ▼
Retriever
      │
      ▼
Documents
```

But later,

the Prompt needs BOTH

* User Question
* Retrieved Documents

Flow

```
                     Question
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
     Passthrough                Retriever
            │                         │
            ▼                         ▼
     Original Question          Documents
                    │
                    ▼
                Prompt
```

Without RunnablePassthrough,

you'd lose the question.

This is why you'll see it everywhere in RAG tutorials.

---

# Another Analogy

Imagine a courier.

Normally

```
Package

↓

Warehouse
```

But suppose you also want a photocopy of the shipping label.

RunnablePassthrough acts like the photocopy machine.

It doesn't change the package.

It simply preserves the original.

---

# Summary

```
RunnablePassthrough

Input
   │
   ▼
Returns exactly the same input

Uses

✔ Keep original data
✔ Feed same input to multiple branches
✔ RAG
✔ RunnableParallel
✔ Debugging
```

---

# Key Takeaways

* `RunnablePassthrough` performs **no transformation**; it simply returns the input unchanged.
* Its real value appears when building multi-step or parallel pipelines where you need to preserve the original input while other branches process it.
* It is commonly used with `RunnableParallel` and is a core building block in RAG pipelines.

---

## 🚀 Next

Now we'll learn **`RunnableAssign`**, where instead of just preserving the input, we'll **attach new information to it**.

That's where LCEL starts feeling like data engineering combined with AI.
    