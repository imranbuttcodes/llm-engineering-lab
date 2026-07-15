LET'S GOOOO BRO!! 🔥🔥

Now we're learning one of the **most important production features** of a Vector Store.

# Chapter 2 — Persistence

---

## The Problem

Suppose you have **50,000 documents**.

You run

```python
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding
)
```

What happens?

```text
Documents
      │
      ▼
Embedding Model
      │
      ▼
50,000 Embeddings Generated
      │
      ▼
Stored in RAM
```

Everything works.

---

Now you close Python.

```text
python app.py

↓

Exit
```

Everything disappears.

```text
❌ Documents

❌ Embeddings

❌ Vector Store
```

Tomorrow...

You run your app again.

What happens?

```text
Generate 50,000 embeddings

↓

Again

↓

Again

↓

Again
```

😵

---

## Is generating embeddings expensive?

Absolutely.

Imagine

```text
100,000 chunks
```

Each embedding call takes

```
15 ms
```

Total time

```
100,000 × 15 ms

≈ 25 minutes
```

Every startup.

Impossible.

---

# Solution

Save the Vector Store to disk.

Exactly like a SQL database.

Instead of RAM

```text
RAM

↓

Disk
```

Now even after restarting

```text
App

↓

Reads existing database

↓

Done
```

---

# Chroma Persistence

The only thing we need is

```python
persist_directory
```

Think of it like

```python
save_folder
```

---

## Example

```python
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory="./chroma_db"
)
```

That's literally it.

---

## What happens internally?

```text
Documents

↓

Embeddings

↓

Chroma

↓

./chroma_db/
```

Now check your project.

```
Project

│
├── app.py
├── chroma_db
│      ├── ...
│      ├── ...
│      └── ...
```

You'll notice a new folder has appeared.

---

# Why is this awesome?

Tomorrow

You don't need

```python
embed_documents()
```

again.

Instead

Simply reopen the database.

---

# Loading Existing Database

This surprises many beginners.

Notice

We are NOT calling

```python
Chroma.from_documents()
```

Why?

Because

The documents are already stored.

Instead

```python
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)
```

Notice

No documents.

No embeddings.

Nothing.

It simply loads the existing database.

---

# Visualization

### First Run

```text
Documents

↓

Embeddings

↓

Save

↓

chroma_db/
```

---

### Second Run

```text
Load chroma_db

↓

Ready
```

Milliseconds.

---

# Complete Example

### First Time

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    Document(page_content="Machine Learning is part of AI."),
    Document(page_content="Pizza comes from Italy."),
]

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory="./chroma_db"
)

print("Database Created!")
```

Run once.

---

Now close Python.

Delete nothing.

Run this instead.

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

results = vector_store.similarity_search("Tell me about AI")

for doc in results:
    print(doc.page_content)
```

Output

```
Machine Learning is part of AI.
```

No embedding generation.

No document loading.

Everything was already stored.

---

# What if I add new documents later?

Suppose next week

Your company uploads

```
new_pdf.pdf
```

Do you recreate the whole database?

No.

You simply add them.

```python
vector_store.add_documents(new_documents)
```

Internally

```text
Existing Database

↓

Generate embeddings

↓

Append

↓

Done
```

---

# Other Useful Methods

## Add one document

```python
vector_store.add_documents([doc])
```

---

## Delete

```python
vector_store.delete(ids=["123"])
```

---

## Count Documents

```python
collection = vector_store._collection

print(collection.count())
```

Output

```
2487
```

---

## Get Documents

```python
collection.get()
```

Returns

```
IDs

Documents

Metadata

Embeddings
```

Useful for debugging.

---

# How does Chroma know which embedding model to use?

Excellent question.

Notice

```python
embedding_function=embedding
```

Why is this required?

Because

When a user asks

```text
What is Machine Learning?
```

Chroma must convert the query into an embedding.

It cannot do that by itself.

So whenever you load an existing database,

you **must provide the same embedding model (or an equivalent compatible one)** that was used when creating the database.

---

# ⚠️ VERY IMPORTANT RULE

Suppose you created your database using

```python
sentence-transformers/all-MiniLM-L6-v2
```

Later

You load it using

```python
BAAI/bge-base-en
```

❌ Bad idea.

Why?

Because each embedding model creates vectors in a different semantic space.

Your stored document vectors and your new query vectors would no longer be directly comparable, leading to poor retrieval quality (and sometimes dimension mismatches if the models have different vector sizes).

**Rule of thumb:** Create and query a vector store with the **same embedding model**.

---

# Industry Pipeline

Now we're getting close to a real RAG system.

```text
PDF Loader
      │
      ▼
Text Splitter
      │
      ▼
Chunks
      │
      ▼
Embedding Model
      │
      ▼
Chroma
(Persistent Database)
      │
      ▼
Similarity Search
      │
      ▼
Retriever
      │
      ▼
LLM
```

---

# 🎯 Up Next (One of the Most Used APIs)

So far we've been using:

```python
vector_store.similarity_search(...)
```

But in almost every LangChain RAG application, you'll instead see:

```python
retriever = vector_store.as_retriever()
```

This isn't just a convenience method—it converts the vector store into a **Retriever**, a standardized interface that every LangChain retrieval chain understands.

Once you understand `as_retriever()`, you'll understand how LangChain plugs vector stores into complete RAG pipelines. That's the next step, and it's one of the most frequently used concepts in production LangChain code. 🚀
