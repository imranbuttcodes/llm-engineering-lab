LET'S GOOO! 🔥

Now we're entering one of the **most powerful Runnable Primitives**.

# RunnableLambda

If you understand `RunnableLambda`, you'll suddenly realize:

> **"Wait... I can put my own Python code anywhere inside an LCEL chain!"**

And that's exactly what makes LangChain so flexible.

---

# The Problem

Suppose you have this chain:

```text
Prompt
   │
   ▼
Model
   │
   ▼
Parser
```

Everything is built using LangChain components.

But what if you want to execute your **own Python function** in the middle?

For example:

* Convert text to uppercase
* Reverse a string
* Count words
* Call an external API
* Query a database
* Perform calculations
* Clean data
* Validate input

How do you insert normal Python code into the chain?

That's where **RunnableLambda** comes in.

---

# Definition

> **RunnableLambda converts a normal Python function into a Runnable.**

So instead of only chaining LangChain components, you can also chain **your own functions**.

---

# Visual

Without RunnableLambda

```text
Prompt
   │
   ▼
Model
   │
   ▼
Parser
```

With RunnableLambda

```text
Prompt
   │
   ▼
Model
   │
   ▼
My Python Function
   │
   ▼
Parser
```

---

# Syntax

```python
from langchain_core.runnables import RunnableLambda

runnable = RunnableLambda(function_name)
```

or

```python
runnable = RunnableLambda(lambda x: ...)
```

---

# Example 1 — Square a Number

Normal Python

```python
def square(x):
    return x * x

print(square(5))
```

Output

```text
25
```

Now make it a Runnable.

```python
from langchain_core.runnables import RunnableLambda

def square(x):
    return x * x

square_runnable = RunnableLambda(square)

result = square_runnable.invoke(5)

print(result)
```

Output

```text
25
```

Notice:

The function didn't change.

Only now it behaves like every other Runnable.

---

# Visual

```text
5
 │
 ▼
RunnableLambda(square)
 │
 ▼
25
```

---

# Example 2 — Convert to Uppercase

```python
from langchain_core.runnables import RunnableLambda

def upper(text):
    return text.upper()

chain = RunnableLambda(upper)

print(chain.invoke("hello"))
```

Output

```text
HELLO
```

---

# Example 3 — Count Words

```python
from langchain_core.runnables import RunnableLambda

def count_words(text):
    return len(text.split())

chain = RunnableLambda(count_words)

print(chain.invoke(
    "Artificial Intelligence is amazing"
))
```

Output

```text
4
```

---

# RunnableLambda inside a Chain

Now comes the exciting part.

Suppose the LLM generates text.

We want to make everything uppercase afterward.

```python
from langchain_core.runnables import RunnableLambda

uppercase = RunnableLambda(
    lambda text: text.upper()
)

chain = prompt | model | parser | uppercase
```

Flow

```text
Prompt

↓

LLM

↓

Parser

↓

Uppercase Function

↓

Final Output
```

---

# Another Example

Suppose the LLM generates

```text
Artificial Intelligence is amazing.
```

Your function

```python
lambda text: len(text)
```

returns

```text
36
```

Chain

```text
Prompt

↓

Model

↓

Parser

↓

Count Characters

↓

36
```

---

# Real Example

Imagine your chatbot generates a paragraph.

You want to know how many words it contains.

```python
def word_count(text):
    return {
        "text": text,
        "words": len(text.split())
    }

counter = RunnableLambda(word_count)

chain = prompt | model | parser | counter
```

Output

```python
{
    "text": "...",
    "words": 182
}
```

No need to modify the model.

Just insert your function.

---

# Example — Cleaning Text

```python
def clean(text):
    return text.strip()

chain = (
    prompt
    | model
    | parser
    | RunnableLambda(clean)
)
```

---

# Example — Reverse Text

```python
def reverse(text):
    return text[::-1]

chain = RunnableLambda(reverse)

print(chain.invoke("Python"))
```

Output

```text
nohtyP
```

---

# Example — Add Metadata

```python
def enrich(text):
    return {
        "answer": text,
        "length": len(text)
    }

chain = (
    prompt
    | model
    | parser
    | RunnableLambda(enrich)
)
```

Output

```python
{
    "answer": "AI is...",
    "length": 420
}
```

---

# RunnableLambda with Dictionaries

Input

```python
{
    "name":"Imran",
    "age":21
}
```

Function

```python
def greet(data):
    return f"Hello {data['name']}"
```

Runnable

```python
chain = RunnableLambda(greet)

print(chain.invoke({
    "name":"Imran",
    "age":21
}))
```

Output

```text
Hello Imran
```

---

# Lambda Function Version

Instead of

```python
def double(x):
    return x * 2

chain = RunnableLambda(double)
```

you can write

```python
chain = RunnableLambda(
    lambda x: x * 2
)
```

Both are equivalent.

---

# Real-World Uses

`RunnableLambda` is commonly used to:

* Transform model output
* Clean text
* Format prompts
* Validate data
* Query databases
* Call REST APIs
* Perform calculations
* Extract fields from dictionaries
* Merge or reshape data
* Add metadata

---

# invoke(), batch(), and stream()

Because `RunnableLambda` is a Runnable, it supports the same execution methods as any other Runnable.

### invoke()

```python
chain.invoke("Hello")
```

### batch()

```python
chain.batch([
    "Hello",
    "World"
])
```

### stream()

While `RunnableLambda` supports `.stream()`, a normal Python function usually returns its result all at once, so there isn't much to stream. Streaming becomes more meaningful with LLMs that generate output token by token.

---

# Summary

```text
RunnableLambda
│
├── Wraps any Python function
├── Becomes a Runnable
├── Can join LCEL chains
├── Supports invoke()
├── Supports batch()
├── Supports stream()
└── Great for custom logic
```

---

# Key Takeaway

Think of `RunnableLambda` as an **adapter**:

```text
Python Function
        │
        ▼
RunnableLambda
        │
        ▼
Runnable
```

It bridges **plain Python code** and the **LangChain Runnable ecosystem**, allowing your custom logic to participate in the same pipelines as prompts, models, parsers, and other Runnables.
