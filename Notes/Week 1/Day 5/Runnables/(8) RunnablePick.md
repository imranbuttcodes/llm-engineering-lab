LET'S GOOOO!! 🔥🔥

Now you've reached the **third member** of this family.

Think of them like CRUD operations on a dictionary:

| Runnable              | Think of it as          |
| --------------------- | ----------------------- |
| `RunnablePassthrough` | Keep everything         |
| `RunnableAssign`      | Add new keys            |
| `RunnablePick`        | Keep only selected keys |

So today we're learning the opposite of `Assign`.

---

# RunnablePick

## Why do we need it?

Imagine you have a dictionary like this:

```python
{
    "question": "What is AI?",
    "answer": "...",
    "summary": "...",
    "quiz": "...",
    "difficulty": "Beginner"
}
```

Now suppose the next chain **only needs** the answer.

Without RunnablePick you'd manually do

```python
data["answer"]
```

But in LCEL we can do it using a Runnable.

That's exactly what RunnablePick does.

---

# Definition

> **RunnablePick selects one or more keys from a dictionary and discards the rest.**

Think of it like filtering.

---

# Visual

Input

```text
{
question,
answer,
summary,
quiz,
difficulty
}
```

↓

RunnablePick(["answer"])

↓

```text
{
answer
}
```

---

# Example 1

```python
from langchain_core.runnables import RunnablePick

pick = RunnablePick("name")

result = pick.invoke({

    "name":"Imran",

    "age":21,

    "city":"Lahore"

})

print(result)
```

Output

```python
{
    "name":"Imran"
}
```

Everything else disappears.

---

# Example 2

Pick multiple keys.

```python
from langchain_core.runnables import RunnablePick

pick = RunnablePick(["name","city"])

result = pick.invoke({

    "name":"Imran",

    "age":21,

    "city":"Lahore",

    "CGPA":3.8

})

print(result)
```

Output

```python
{
    "name":"Imran",

    "city":"Lahore"
}
```

---

# Visual

Before

```text
Name
Age
City
CGPA
```

↓

Pick

↓

```text
Name
City
```

---

# Example 3 — AI Pipeline

Suppose an earlier chain produced

```python
{
    "question":"Explain AI",

    "summary":"...",

    "quiz":"...",

    "difficulty":"Intermediate"
}
```

Now another LLM only needs the summary.

```python
pick = RunnablePick("summary")
```

Output

```python
{
    "summary":"..."
}
```

---

# Example 4 — With Assign

Suppose we build this pipeline.

Input

```python
{
    "number":5
}
```

↓

Assign

```python
{
    "number":5,

    "square":25,

    "cube":125
}
```

↓

Pick

```python
RunnablePick(["square"])
```

↓

Output

```python
{
    "square":25
}
```

Notice what happened?

Assign made the dictionary larger.

Pick made it smaller.

---

# Complete Example

```python
from langchain_core.runnables import (
    RunnableAssign,
    RunnableParallel,
    RunnableLambda,
    RunnablePick
)

assign = RunnableAssign(

    RunnableParallel({

        "square": RunnableLambda(
            lambda x: x["number"] ** 2
        ),

        "cube": RunnableLambda(
            lambda x: x["number"] ** 3
        )

    })

)

pick = RunnablePick(["cube"])

chain = assign | pick

result = chain.invoke({

    "number":4

})

print(result)
```

Output

```python
{
    "cube":64
}
```

---

# Example 5 — LLM Example

Suppose an AI pipeline returns

```python
{
    "report":"Long report...",

    "summary":"Short summary...",

    "quiz":"MCQs...",

    "flashcards":"..."
}
```

You only want the summary.

```python
pick = RunnablePick("summary")
```

Output

```python
{
    "summary":"Short summary..."
}
```

---

# Real-World Analogy

Imagine a university database.

```text
Name
Age
Email
Phone
CGPA
Address
Department
```

The Accounts Office only needs

* Name
* CGPA

RunnablePick acts like a filter.

Output

```text
Name
CGPA
```

Everything else is ignored.

---

# Another Analogy

Imagine you have a backpack full of books.

```text
📘 Math
📗 Physics
📙 English
📕 Chemistry
📔 Biology
```

Tomorrow's exam is only Physics.

RunnablePick says

> Keep Physics.

Leave the rest behind.

---

# Assign vs Pick

This is the easiest way to remember them.

### RunnableAssign

Adds keys.

```python
{
"name":"Imran"
}
```

↓

```python
{
"name":"Imran",

"CGPA":3.9
}
```

---

### RunnablePick

Keeps selected keys.

```python
{
"name":"Imran",

"CGPA":3.9,

"City":"Lahore"
}
```

↓

```python
{
"CGPA":3.9
}
```

---

# Comparison of All Four

| Runnable              | What it does                 | Input Changed? | Output             |
| --------------------- | ---------------------------- | -------------- | ------------------ |
| `RunnableLambda`      | Transform data               | ✅ Yes          | Any object         |
| `RunnablePassthrough` | Return input unchanged       | ❌ No           | Same object        |
| `RunnableAssign`      | Add new keys to a dictionary | ➕ Yes          | Bigger dictionary  |
| `RunnablePick`        | Keep only selected keys      | ✂️ Yes         | Smaller dictionary |

---

# The Family Tree

```text
                    Dictionary
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  RunnableLambda   RunnableAssign   RunnablePick
         │               │               │
   Transform Data    Add New Keys    Remove Unwanted Keys
                         │
                         ▼
                RunnablePassthrough
                  (Keep Everything)
```

> A small correction to the diagram: **`RunnablePassthrough` isn't really "under" the others—it operates independently.** A better mental model is:
>
> * **Lambda** → transform
> * **Passthrough** → preserve
> * **Assign** → enrich
> * **Pick** → filter

---

# 🎯 When do you use each?

| Situation                                  | Runnable              |
| ------------------------------------------ | --------------------- |
| Modify or calculate a value                | `RunnableLambda`      |
| Keep the original input for later          | `RunnablePassthrough` |
| Add AI-generated or computed fields        | `RunnableAssign`      |
| Pass only specific fields to the next step | `RunnablePick`        |

---

## 🚀 Congratulations!

You've now covered the **core Runnable Primitives** used in most LCEL pipelines:

* ✅ `RunnableLambda`
* ✅ `RunnableSequence`
* ✅ `RunnableParallel`
* ✅ `RunnableBranch`
* ✅ `RunnablePassthrough`
* ✅ `RunnableAssign`
* ✅ `RunnablePick`

With these, you can already build surprisingly sophisticated AI workflows by combining, branching, enriching, and filtering data as it moves through your chains.
