LET'S GOOOO! 🔥🚀

Now we'll learn the **methods that every Runnable has**. These are the methods you'll use throughout LangChain.

# Runnable Methods

Every Runnable supports these core methods:

```text
Runnable
│
├── invoke()      ⭐ Most Common
├── batch()
├── stream()
├── ainvoke()
├── abatch()
└── astream()
```

We'll cover them one by one.

---

# 1. invoke()

## What is it?

`invoke()` executes a Runnable on **one input**.

Think of it as:

> **One Input ➜ One Output**

---

## Visual

```text
Input
  │
  ▼
Runnable
  │
  ▼
Output
```

---

## Example 1

Prompt Template

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic}"
)

result = prompt.invoke({
    "topic": "Artificial Intelligence"
})

print(result)
```

Flow

```text
{"topic":"AI"}

↓

PromptTemplate

↓

Explain Artificial Intelligence
```

---

## Example 2

Model

```python
response = model.invoke(
    "What is AI?"
)
```

Flow

```text
Question

↓

LLM

↓

Answer
```

---

## Example 3

Whole Chain

```python
chain = prompt | model | parser

result = chain.invoke({
    "topic":"Python"
})
```

Instead of calling

```python
prompt.invoke()

model.invoke()

parser.invoke()
```

only one call is needed.

---

# Why invoke() Exists

Without invoke

```python
prompt_text = prompt.invoke(data)

response = model.invoke(prompt_text)

answer = parser.invoke(response)
```

With Chains

```python
chain.invoke(data)
```

Everything executes automatically.

---

# When to Use invoke()

Use it when you have

* One question
* One prompt
* One report
* One email
* One document

Basically,

**one input at a time.**

---

# 2. batch()

Suppose you have

```text
100 Questions
```

Should you write

```python
for question in questions:
    chain.invoke(question)
```

You could...

But that's inefficient.

---

Instead,

use

```python
chain.batch(...)
```

---

## Visual

Instead of

```text
Question 1

↓

Runnable

↓

Answer 1

Question 2

↓

Runnable

↓

Answer 2

Question 3

↓

Runnable

↓

Answer 3
```

batch()

```text
Questions

↓

Runnable

↓

Answers
```

---

## Example

```python
questions = [

    {"topic":"AI"},

    {"topic":"Python"},

    {"topic":"Java"}

]

results = chain.batch(questions)
```

Output

```python
[
    "AI answer",

    "Python answer",

    "Java answer"
]
```

Notice

Input

```python
List
```

Output

```python
List
```

---

## Why Faster?

Many providers process requests concurrently.

Instead of waiting

```text
1

↓

2

↓

3

↓

4
```

they do

```text
1

2

3

4

↓

All Together
```

Much faster.

---

# invoke() vs batch()

| invoke()        | batch()         |
| --------------- | --------------- |
| One input       | Multiple inputs |
| One output      | List of outputs |
| Simple requests | Bulk processing |

---

# Example Comparison

invoke

```python
chain.invoke({

    "topic":"Python"

})
```

batch

```python
chain.batch([

    {"topic":"Python"},

    {"topic":"AI"},

    {"topic":"ML"}

])
```

---

# 3. stream()

This one is REALLY useful.

Normally,

LLMs wait until everything is generated.

```text
Thinking...

Thinking...

Thinking...

Entire Answer
```

User waits.

---

Streaming changes this.

Instead of waiting,

tokens arrive immediately.

```text
H

He

Hel

Hell

Hello

Hello!

Hello! AI

...
```

Exactly like ChatGPT.

---

## Visual

Without Streaming

```text
Input

↓

Thinking...

↓

Thinking...

↓

Thinking...

↓

Answer
```

---

With Streaming

```text
Input

↓

H

↓

He

↓

Hel

↓

Hell

↓

Hello
```

---

## Example

```python
for chunk in chain.stream({

    "topic":"Artificial Intelligence"

}):

    print(chunk, end="")
```

Output

```text
Artificial

 Intelligence

 is

 the

 simulation

 of...
```

Notice

The answer appears gradually.

---

## Why Streaming?

Better user experience.

Nobody likes waiting 15 seconds.

Streaming makes the application feel much faster.

---

# invoke() vs stream()

invoke

```text
Wait...

↓

Entire Answer
```

stream

```text
Answer

appears

little

by

little
```

---

# 4. ainvoke()

The "a" means

**Asynchronous**

Instead of

```python
invoke()
```

you use

```python
await ainvoke()
```

---

Example

```python
result = await chain.ainvoke({

    "topic":"AI"

})
```

Mostly used in

* FastAPI
* Async APIs
* Production servers

---

# 5. abatch()

Async version of batch.

```python
results = await chain.abatch(
    questions
)
```

---

# 6. astream()

Async streaming.

```python
async for chunk in chain.astream(
    data
):

    print(chunk)
```

Mostly used inside async web applications.

---

# Complete Runnable Family

```text
Runnable

│

├── invoke()

├── batch()

├── stream()

├── ainvoke()

├── abatch()

└── astream()
```

---

# Which One Should I Use?

### Learning

```python
invoke()
```

---

### Multiple Inputs

```python
batch()
```

---

### Chat Applications

```python
stream()
```

---

### FastAPI

```python
ainvoke()
```

---

### Async Multiple Inputs

```python
abatch()
```

---

### Async Streaming

```python
astream()
```

---

# Real Example

Imagine you're building an AI Teacher.

One student

```python
invoke()
```

---

100 students

```python
batch()
```

---

ChatGPT-like typing effect

```python
stream()
```

---

FastAPI backend

```python
ainvoke()
```

---

# Summary

```text
Runnable Methods
│
├── invoke()
│      One Input → One Output
│
├── batch()
│      Multiple Inputs → Multiple Outputs
│
├── stream()
│      Output token-by-token
│
├── ainvoke()
│      Async invoke()
│
├── abatch()
│      Async batch()
│
└── astream()
       Async stream()
```

---

# 💡 One Important Thing to Know

You've already used `invoke()` many times. The next three methods—`batch()`, `stream()`, and their async versions—are **not new types of Runnables**. They are simply **different ways of executing the exact same Runnable**.

For example, this chain:

```python
chain = prompt | model | parser
```

can be executed in all of these ways:

```python
# Single input
chain.invoke({"topic": "AI"})

# Multiple inputs
chain.batch([
    {"topic": "AI"},
    {"topic": "Python"}
])

# Streaming output
for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="")
```

The chain doesn't change—**only the execution method changes**.

---

## 🚀 Next Up

Now we'll move to the first specialized Runnable:

### **`RunnableLambda`**

This is where Runnables become much more powerful, because you'll be able to plug **your own Python functions directly into an LCEL pipeline**. It's one of the most useful concepts for building real-world AI applications.
