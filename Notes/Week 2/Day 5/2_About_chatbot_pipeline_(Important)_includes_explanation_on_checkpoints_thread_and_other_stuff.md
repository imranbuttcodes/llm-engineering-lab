Exactly. This is one of the most important concepts in LangGraph persistence.

---

# How are checkpoints created?

Think of a checkpoint as a **snapshot of the workflow state**.

Whenever a node finishes executing, LangGraph automatically saves:

* current state
* next node to execute
* thread id
* metadata
* parent checkpoint

So after every successful node execution, a checkpoint is written by the checkpointer.

---

# Example

Suppose you have

```text
START
   │
   ▼
Generate Joke
   │
   ▼
Explain Joke
   │
   ▼
END
```

Initial state

```python
{
    "topic": "Python"
}
```

---

### Before execution

No checkpoints.

---

## Node 1 runs

```
Generate Joke
```

returns

```python
{
    "joke": "Python is so easy...
}
```

LangGraph immediately stores

```
Checkpoint #1

State

topic = Python

joke = ...
```

Then moves to

```
Explain Joke
```

---

## Node 2 runs

returns

```python
{
    "explanation": ...
}
```

LangGraph stores

```
Checkpoint #2

topic
joke
explanation
```

Workflow ends.

---

So yes,

> **every node execution creates a checkpoint.**

---

# What if a node crashes?

Suppose

```
Generate Joke
```

completed.

Checkpoint saved.

Then

```
Explain Joke
```

takes 30 seconds.

You interrupt the notebook.

The latest checkpoint is still

```
After Generate Joke
```

Later

```python
workflow.invoke(
    None,
    config=config
)
```

LangGraph loads

```
Checkpoint #1
```

and continues from

```
Explain Joke
```

instead of restarting.

That's exactly why Fault Tolerance works.

---

# Does every thread have its own checkpoints?

**YES.**

This is the most important thing.

Imagine

```
Thread A

User:
Tell me a joke
```

and

```
Thread B

User:
Teach me AI
```

Internally SQLite stores something conceptually like

```
Thread A

Checkpoint 1
Checkpoint 2
Checkpoint 3


Thread B

Checkpoint 1
Checkpoint 2
Checkpoint 3
Checkpoint 4
```

They never mix.

---

# Visualize it

```
Thread A

Start
  │
CP1
  │
CP2
  │
CP3
  │
END
```

while simultaneously

```
Thread B

Start
 │
CP1
 │
CP2
 │
CP3
 │
CP4
 │
END
```

Each thread is completely independent.

---

# Why do we pass thread_id?

Because LangGraph asks

> "Which workflow's checkpoints should I load?"

When you do

```python
config = {
    "configurable": {
        "thread_id": "123"
    }
}
```

LangGraph says

```
Open thread 123

Load latest checkpoint

Resume from there
```

If instead you use

```python
thread_id = "456"
```

it loads

```
Thread 456
```

which has an entirely different conversation.

---

# What does a checkpoint actually contain?

A checkpoint is much more than just messages.

It contains

```
State

↓

messages

conversation_name

tool_results

variables

custom state fields

current node

next node

metadata

parent checkpoint

timestamp
```

Basically **everything required to continue execution**.

---

# Why can we do Time Travel?

Suppose your history is

```
CP1

↓

CP2

↓

CP3

↓

CP4
```

You can say

```python
checkpoint_id = CP2
```

LangGraph loads

```
State at CP2
```

Then

```python
workflow.invoke(None, config=...)
```

Execution resumes **from that exact point**, creating a **new branch** while leaving the original history intact.

```
Original

CP1
 │
CP2
 │
CP3
 │
CP4


New branch

CP1
 │
CP2
 │
CP5
 │
CP6
```

Nothing is overwritten.

---

# How does this work in your chatbot?

Every user message triggers a new workflow execution.

For example:

```
You:
Hi
```

Workflow:

```
START

↓

Generate Title (only first message)

↓

Chat Node

↓

END
```

Checkpoints:

```
CP1
(after Generate Title)

↓

CP2
(after Chat Node)
```

Next message:

```
What is AI?
```

LangGraph loads **CP2**, appends the new `HumanMessage`, executes the graph again, and creates new checkpoints.

```
CP1

↓

CP2

↓

CP3

↓

CP4
```

This is why your chatbot remembers the conversation.

---

## Interview answer

> **LangGraph automatically creates a checkpoint after every node execution. Each thread maintains its own independent checkpoint history, allowing workflows to resume from failures, support time travel, and maintain isolated conversation memory.**
