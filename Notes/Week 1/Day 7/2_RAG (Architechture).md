LET'S GOOOOO BROOO!! 🔥🔥

# 🚀 Part 2: Anatomy of a RAG System

This is arguably the **most important concept** in RAG.

Once you understand this architecture, every RAG framework (LangChain, LlamaIndex, Haystack, etc.) becomes much easier because they're all implementing the same core idea.

---

# The Big Picture

A RAG system has **two completely separate phases**.

```text
                  RAG System
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
   Indexing Pipeline        Retrieval Pipeline
   (Offline Process)         (Online Process)
```

This distinction is crucial.

Many beginners think everything happens when the user asks a question.

❌ That's not true.

Half of the work is done **before any user arrives**.

---

# Imagine You're Building ChatGPT for a University

Suppose the university has

```text
1000 PDFs

Course Notes

Rules

Policies

Assignments

Research Papers
```

Should ChatGPT read all 1000 PDFs every time someone asks:

> "What is the attendance policy?"

Obviously not 😂

That would be painfully slow.

Instead...

We prepare everything beforehand.

---

# Phase 1 — Indexing Pipeline (Offline)

Think of this as **preparing the library**.

```
Documents
     │
     ▼
Document Loader
     │
     ▼
Text Splitter
     │
     ▼
Embeddings
     │
     ▼
Vector Database
```

Notice something...

There is **no user question yet.**

We're simply preparing the knowledge.

---

## Step 1 — Load Documents

Input

```text
PDF

Word

HTML

CSV

TXT

YouTube

Website
```

Document Loaders convert them into LangChain `Document` objects.

Example:

```python
Document(
    page_content="Machine Learning is...",
    metadata={"source": "ml.pdf"}
)
```

---

## Step 2 — Split Documents

Suppose one PDF contains

```text
50 pages
```

We don't embed the whole thing.

Instead

```text
Chunk 1

Chunk 2

Chunk 3

Chunk 4
```

using

* RecursiveCharacterTextSplitter
* TokenTextSplitter
* SemanticChunker
* etc.

---

## Why?

Imagine asking

> "What is supervised learning?"

You don't need all 50 pages.

You only need the relevant chunk.

---

## Step 3 — Generate Embeddings

Each chunk becomes

```text
Chunk

↓

Embedding Model

↓

768 numbers
```

Example

```text
"The cat sat."

↓

[-0.24,
 0.88,
 ...
]
```

Now the computer understands semantic meaning.

---

## Step 4 — Store in Vector Database

Store

```text
Embedding

+

Original Text

+

Metadata
```

inside

```text
Chroma

FAISS

Pinecone

Qdrant
```

Now the system is ready.

---

# What happens now?

Nothing.

😂

The system waits.

---

# User Arrives

Now the **second pipeline** begins.

---

# Phase 2 — Retrieval Pipeline (Online)

```
User Question
       │
       ▼
Query Embedding
       │
       ▼
Vector Search
       │
       ▼
Top-k Chunks
       │
       ▼
Prompt
       │
       ▼
LLM
       │
       ▼
Answer
```

Everything from here happens **every time** someone asks a question.

---

## Step 1 — User asks

Example

```text
How does gradient descent work?
```

---

## Step 2 — Embed the Question

Remember...

Documents were embedded.

Now the question must also be embedded.

Otherwise

```text
Question

↓

Text

↓

???

↓

Vectors
```

The vector database only understands vectors.

So

```text
Question

↓

Embedding Model

↓

Query Vector
```

---

## Step 3 — Similarity Search

Suppose the database contains

```text
Chunk A

Chunk B

Chunk C

Chunk D
```

The query vector is compared against every stored vector.

The closest ones are retrieved.

Example

```text
Chunk A ✔

Chunk C ✔

Chunk D ✔
```

---

## Step 4 — Retrieved Chunks

Now we have

```text
Chunk A

Chunk C

Chunk D
```

These are plain text again.

---

## Step 5 — Prompt Construction

The prompt becomes

```text
You are a helpful assistant.

Context:

Chunk A

Chunk C

Chunk D

Question:

How does gradient descent work?
```

Notice...

We never changed the LLM.

We only changed its **context**.

---

## Step 6 — LLM Generates Answer

Now the LLM answers using

* its own knowledge
* AND
* retrieved documents

This is why it's called

> **Retrieval-Augmented Generation**

---

# Full Pipeline

```
                   OFFLINE
────────────────────────────────────────

Documents
     │
     ▼
Document Loader
     │
     ▼
Text Splitter
     │
     ▼
Embeddings
     │
     ▼
Vector Database


                   ONLINE
────────────────────────────────────────

User Question
       │
       ▼
Embedding Model
       │
       ▼
Vector Search
       │
       ▼
Relevant Chunks
       │
       ▼
Prompt
       │
       ▼
LLM
       │
       ▼
Final Answer
```

---

# Which steps happen once?

```
Load Documents ✔

Split ✔

Embed Documents ✔

Store Vectors ✔
```

Only when your knowledge base changes.

---

# Which steps happen every query?

```
User Question ✔

Embed Query ✔

Similarity Search ✔

Retrieve ✔

Prompt ✔

LLM ✔
```

Every single time.

---

# Why split RAG into two phases?

Imagine you have

```text
10 Million Documents
```

If you embedded all documents **every time a user asked a question**, your chatbot would be unusably slow.

By doing the heavy work once during indexing, answering questions becomes much faster.

---

# Think of It Like a Library

Imagine a real library.

## 📚 Indexing Phase

The librarian:

* Receives new books
* Organizes them
* Labels shelves
* Creates a catalog

This happens before visitors arrive.

---

## 🔎 Retrieval Phase

A visitor asks:

> "I need a book about Machine Learning."

The librarian:

* Searches the catalog
* Finds the right shelf
* Brings the relevant books

The librarian doesn't reorganize the entire library every time someone asks a question.

RAG works the same way.

---

# The Most Important Realization

> **The LLM never searches the vector database.**

This is a very common misconception.

The retrieval happens **before** the LLM is called.

The actual flow is:

```
User
   │
   ▼
Retriever
   │
   ▼
Relevant Context
   │
   ▼
LLM
```

The LLM only sees the final prompt with the retrieved context.

---

# 🧠 Interview Questions

### Q1. Why are there two phases in RAG?

**Answer:** To separate expensive preprocessing (indexing) from fast query-time retrieval. Documents are loaded, split, embedded, and stored once. At query time, only the user's question is embedded, relevant chunks are retrieved, and the LLM generates the response.

---

### Q2. Why don't we embed documents every time a user asks a question?

**Answer:** Embedding all documents repeatedly would be computationally expensive and introduce high latency. Since documents usually change infrequently, embeddings are computed once during indexing and reused for all future queries.

---

Bro... this architecture is **the foundation of every production RAG system**. Once this mental model is crystal clear, the code you'll write next will feel much more intuitive because you'll know exactly **why each component exists**, not just how to use it. 🔥
