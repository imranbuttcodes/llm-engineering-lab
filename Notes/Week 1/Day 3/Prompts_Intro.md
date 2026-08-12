# Static vs Dynamic Prompts

## What is a Prompt?

A **prompt** is the instruction or input that we give to a Large Language Model (LLM) to generate a response.

Example:

```text
Explain what Machine Learning is.
```

---

# Static Prompt

A **Static Prompt** is a prompt whose content is completely fixed. It never changes while the program is running.

### Example

```python
prompt = """
You are an experienced Computer Science teacher.

Explain what Artificial Intelligence is.
"""
```

Every time the model is called, it receives exactly the same prompt.

### When to use

* Fixed instructions
* Testing models
* Simple scripts
* Constant chatbot behavior

### Advantages

* Easy to write
* Predictable responses
* Good for quick experiments

### Disadvantages

* Cannot accept user input
* Not reusable
* Very limited flexibility

---

# Dynamic Prompt

A **Dynamic Prompt** contains placeholders (variables) whose values are provided at runtime.

Instead of writing one prompt for every situation, we create a template and fill in the missing values.

### Example

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
Explain the topic: {topic}

Difficulty Level: {level}
""")
```

Later we provide the values:

```python
final_prompt = prompt.invoke({
    "topic": "Neural Networks",
    "level": "Beginner"
})
```

The model actually receives:

```text
Explain the topic: Neural Networks

Difficulty Level: Beginner
```

The same template can now explain any topic at any difficulty level.

---

# Why Dynamic Prompts are Better

Imagine you're building an AI learning assistant.

With a **Static Prompt**, you'd need to rewrite the prompt every time:

```text
Explain Python.
Explain Java.
Explain C++.
Explain AI.
Explain ML.
```

With a **Dynamic Prompt**, one template handles everything:

```text
Explain {topic}
Difficulty: {level}
```

Only the values change.

---

# Real-Life Analogy

Imagine a school exam paper.

### Static Prompt

A printed exam:

> Explain Artificial Intelligence.

Every student gets the exact same question.

---

### Dynamic Prompt

A form with blanks:

> Explain __________.

The teacher can fill in:

* Python
* AI
* Databases
* Networking
* Machine Learning

The structure stays the same; only the content changes.

---

# Static vs Dynamic Prompt

| Static Prompt    | Dynamic Prompt              |
| ---------------- | --------------------------- |
| Fixed text       | Uses variables/placeholders |
| Never changes    | Changes based on user input |
| Less flexible    | Highly flexible             |
| Good for testing | Best for real applications  |
| Not reusable     | Reusable                    |

---

# In LangChain

Static Prompt:

```python
prompt = """
Explain Artificial Intelligence.
"""
```

Dynamic Prompt:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} for a {level} learner."
)
```

---

# Key Takeaway

* **Static Prompt = Fixed instruction.**
* **Dynamic Prompt = Template + Variables.**

Almost every real-world AI application—such as ChatGPT clones, AI tutors, customer support bots, RAG systems, and AI agents—uses **dynamic prompts**, because they allow the same prompt template to handle countless different user requests.
