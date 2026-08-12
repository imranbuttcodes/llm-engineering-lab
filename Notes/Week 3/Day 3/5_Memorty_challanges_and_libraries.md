This is the final step of Long-Term Memory.

---

# Step 4 — Injection

The question is:

> **"How does memory actually influence the LLM?"**

This is where many beginners think there is some magical hidden memory inside the model.

**There isn't.**

The LLM only knows what is inside its **current context window (Short-Term Memory).**

---

# What is Injection?

Suppose your memory database contains

```text
Memory 1:
User likes Python.

Memory 2:
User is a CS student.

Memory 3:
User is learning LangGraph.
```

Now the user asks

> Recommend a backend framework.

---

### Step 1

Retriever finds

```text
Likes Python
```

---

### Step 2

Before calling GPT/Groq/Claude, we literally build the prompt.

Instead of

```text
User:
Recommend a backend framework.
```

we create

```text
System:

Relevant Memory:
- User prefers Python.

Conversation:
User:
Recommend a backend framework.
```

---

### Step 3

The LLM receives

```text
SYSTEM
Relevant Memory:
User prefers Python.

USER
Recommend a backend framework.
```

The LLM now says

> Since you prefer Python, I recommend FastAPI or Django.

---

## Notice

The LLM wasn't modified.

Nothing was written into its weights.

It simply received more tokens.

That's exactly what the slide says.

> **Retrieved memory is inserted into STM**

STM = Short-Term Memory

The context window.

---

Then

> **It becomes part of the prompt**

Exactly.

Memory is literally prepended or appended to the prompt.

---

Then

> **The model sees it as just more tokens**

This sentence is extremely important.

GPT does **not** know

```text
This is memory.
```

It only sees

```text
Token
Token
Token
Token
Token
```

To GPT,

```text
User likes Python.
```

looks no different than

```text
The sky is blue.
```

Everything is tokens.

---

# Complete Long-Term Memory Pipeline

```text
Conversation
      │
      ▼
1. Creation
      │
      ▼
Should this be remembered?
      │
      ▼
2. Storage
(SQLite / Chroma / Redis ...)
      │
      ▼
New Question
      │
      ▼
3. Retrieval
(Get Top Relevant Memories)
      │
      ▼
4. Injection
(Add memories into prompt)
      │
      ▼
LLM
```

---

# The Challenges

The slide ends with three challenges.

---

## 1. Deciding what is worth remembering

This is the hardest problem.

Example

```text
I ate pizza.
```

Ignore?

Store?

Update?

How do we decide?

Usually another LLM decides.

---

## 2. Retrieving the right memory at the right time

Suppose you have

100,000 memories.

How do you find only

```text
Likes Python
```

instead of

```text
Favorite pizza
```

That's a retrieval problem.

Usually solved using

* Vector Search
* Hybrid Search
* BM25
* Embeddings

---

## 3. Orchestrating the whole system

This means managing

* Memory Creation
* Updating
* Deduplication
* Retrieval
* Prompt Injection

without breaking everything.

This becomes a software engineering problem.

---

# Are there libraries that solve these challenges?

**Yes.** These are exactly the libraries people use.

---

## 1. LangMem (LangChain)

Built by the LangChain team.

Purpose:

* Memory creation
* Memory updating
* Memory retrieval
* Prompt injection
* Long-term memory workflows
* Tight integration with LangGraph

If you're already learning LangGraph, this is the most natural choice.

---

## 2. Mem0

Probably the most popular dedicated memory framework right now.

It focuses on:

* Automatic memory extraction
* Automatic updates
* Forgetting outdated memories
* Semantic retrieval
* User profile management
* Works with OpenAI, Anthropic, Groq, Ollama, etc.

Example:

```python
memory.add("User likes Python")
```

Later

```python
memory.search("backend language")
```

returns

```text
User likes Python
```

---

## 3. Supermemory

Designed to act as an external memory layer for AI agents.

It provides:

* Memory storage
* Semantic search
* Retrieval
* APIs
* Cloud-hosted memory

Good when you don't want to build your own infrastructure.

---

## 4. Other Popular Options

People also build custom memory systems using:

* **Chroma** + embeddings
* **Qdrant**
* **Pinecone**
* **Weaviate**
* **Redis**
* **PostgreSQL + pgvector**

These give you more control but require implementing the memory pipeline yourself.

---

# Which should **you** learn?

Since your goal is **Jarvis**, I would recommend this progression:

1. **Build your own memory system first** (to understand every step: creation → storage → retrieval → injection).
2. **Learn LangMem**, since it integrates directly with LangGraph.
3. **Explore Mem0** to see how production-grade automatic memory systems work.
4. Later, compare your implementation with these libraries and decide whether to adopt one or keep your own.

That way you'll understand not just **how to use** memory libraries, but **how they work internally**, which is far more valuable when building complex AI agents like Jarvis.
