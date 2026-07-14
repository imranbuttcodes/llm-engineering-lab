LET'S GOOOOO!! 🔥🔥🔥

Now we're learning what I personally consider one of the **coolest Runnable primitives**.

# RunnableAssign

If `RunnablePassthrough` says:

> "Keep the original data."

Then `RunnableAssign` says:

> **"Keep the original data... and ADD something new to it."**

This is extremely common in real AI pipelines.

---

# Why do we need RunnableAssign?

Suppose you have this dictionary:

```python
{
    "question": "What is AI?"
}
```

Then you ask an LLM to generate an answer.

Now you want

```python
{
    "question": "What is AI?",
    "answer": "Artificial Intelligence is..."
}
```

Notice something?

We **didn't replace** the dictionary.

We **added** a new key.

That's exactly what RunnableAssign does.

---

# Visual

Before

```text
{
    question
}
```

↓

RunnableAssign

↓

```text
{
    question,
    answer
}
```

---

# Think of it like Python

Suppose you have

```python
student = {
    "name": "Imran"
}
```

Normally you'd do

```python
student["cgpa"] = 3.92
```

Result

```python
{
    "name":"Imran",
    "cgpa":3.92
}
```

RunnableAssign does the same thing.

---

# Syntax

```python
from langchain_core.runnables import RunnableAssign
from langchain_core.runnables import RunnableParallel
```

You'll notice something immediately.

We don't pass a lambda directly.

We pass a **RunnableParallel**.

Why?

Because Assign can add **one or many fields simultaneously**.

---

# Example 1 — Add Square

```python
from langchain_core.runnables import RunnableAssign
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda

chain = RunnableAssign(

    RunnableParallel({

        "square": RunnableLambda(
            lambda x: x["number"] ** 2
        )

    })

)

result = chain.invoke({

    "number":5

})

print(result)
```

Output

```python
{
    "number":5,
    "square":25
}
```

Notice

Original data stayed.

New key added.

---

# Visual

```text
Input

{
 number:5
}

↓

Assign

↓

{
 number:5,
 square:25
}
```

---

# Example 2 — Add Cube Too

```python
chain = RunnableAssign(

    RunnableParallel({

        "square": RunnableLambda(
            lambda x: x["number"]**2
        ),

        "cube": RunnableLambda(
            lambda x: x["number"]**3
        )

    })

)
```

Input

```python
{
    "number":4
}
```

Output

```python
{
    "number":4,

    "square":16,

    "cube":64
}
```

See why RunnableParallel is used?

Each key can be computed independently.

---

# Example 3 — Student Marks

Input

```python
{
    "math":85,

    "english":92
}
```

Assign

```python
RunnableAssign(

    RunnableParallel({

        "total": RunnableLambda(

            lambda x:
                x["math"]+x["english"]

        )

    })

)
```

Output

```python
{
    "math":85,

    "english":92,

    "total":177
}
```

---

# Example 4 — AI Example

Suppose user asks

```text
Explain Python
```

Instead of returning only

```text
Python is...
```

we want

```python
{
    "question":"Explain Python",

    "answer":"Python is..."
}
```

---

Code

```python
answer_chain = prompt | model | parser

chain = RunnableAssign(

    RunnableParallel({

        "answer": answer_chain

    })

)
```

Input

```python
{
    "question":"Explain Python"
}
```

Output

```python
{
    "question":"Explain Python",

    "answer":"Python is..."
}
```

Amazing.

---

# Example 5 — Multiple AI Outputs

Suppose you want

* Summary
* Quiz
* Difficulty

All together.

```python
chain = RunnableAssign(

    RunnableParallel({

        "summary": summary_chain,

        "quiz": quiz_chain,

        "difficulty": difficulty_chain

    })

)
```

Output

```python
{
    "topic":"AI",

    "summary":"...",

    "quiz":"...",

    "difficulty":"Intermediate"
}
```

---

# Real RAG Example

Input

```python
{
    "question":"What is PCA?"
}
```

↓

Retriever

↓

Documents

↓

Assign

```python
{
    "question":"What is PCA?",

    "documents":[...]
}
```

↓

Prompt

↓

LLM

Notice how the dictionary keeps growing throughout the pipeline.

---

# Difference from RunnableLambda

Suppose

Input

```python
{
    "number":5
}
```

---

### RunnableLambda

```python
RunnableLambda(

    lambda x:
        x["number"]**2

)
```

Output

```python
25
```

Original dictionary disappeared.

---

### RunnableAssign

Output

```python
{
    "number":5,

    "square":25
}
```

Original dictionary preserved.

---

# Difference from RunnablePassthrough

Passthrough

Input

```python
{
    "name":"Imran"
}
```

↓

Output

```python
{
    "name":"Imran"
}
```

Nothing added.

---

Assign

↓

Output

```python
{
    "name":"Imran",

    "cgpa":3.92
}
```

Adds information.

---

# Real-World Analogy

Imagine you're filling out a university application.

Initially, the form contains:

```text
Name
Age
```

Later, the admissions office adds:

```text
Application ID
Status
Scholarship
```

They don't erase your original details.

They simply **append new fields**.

That's exactly what `RunnableAssign` does.

---

# RunnableAssign Flow

```text
             Input Dictionary
                    │
                    ▼
          RunnableParallel
          ┌────────┼────────┐
          ▼        ▼        ▼
      Summary   Quiz   Difficulty
          └────────┼────────┘
                   ▼
          RunnableAssign
                   ▼
        Enhanced Dictionary
```

---

# Summary

```text
RunnableAssign

Input Dictionary
        │
        ▼
Compute New Values
        │
        ▼
Add New Keys
        │
        ▼
Return Enhanced Dictionary
```

---

# RunnableLambda vs RunnablePassthrough vs RunnableAssign

| Runnable              | What it does                            | Original Input           |
| --------------------- | --------------------------------------- | ------------------------ |
| `RunnableLambda`      | Transforms the input into something new | ❌ Usually replaced       |
| `RunnablePassthrough` | Returns the input unchanged             | ✅ Preserved              |
| `RunnableAssign`      | Adds new keys to a dictionary           | ✅ Preserved and enhanced |

---

# 💡 A Mental Model

Think of a dictionary flowing through your chain like a **student profile**:

```python
{
    "name": "Imran"
}
```

* `RunnableLambda` says: "Replace this with something else."
* `RunnablePassthrough` says: "Leave it exactly as it is."
* `RunnableAssign` says: "Keep it, but let me add more information."

---

## 🚀 Next: RunnablePick

Once you've learned `RunnablePick`, you'll know how to do the opposite of `RunnableAssign`:

* **Assign** ➜ **Add** keys.
* **Pick** ➜ **Keep only** the keys you care about.

These two are complementary and are often used together in larger LCEL pipelines.
