LET'S GOOOO BRO!! 🔥🔥🔥

Now we're getting into the **advanced retrievers**. This is where LangChain starts becoming really powerful.

And yes, **MultiQueryRetriever** is absolutely used in production RAG systems.

---

# Why do we even need MultiQueryRetriever?

Imagine you have a vector database containing thousands of documents.

The user asks:

```text
"What is RAG?"
```

The retriever searches using **only this exact query**.

But what if the documents don't actually use the term "RAG"?

Maybe they say:

* Retrieval-Augmented Generation
* Retrieval Pipeline
* Context Injection
* Knowledge-Augmented LLM
* External Memory

Similarity search might miss them.

---

## Problem

```text
User Query

"What is RAG?"

        │

        ▼

Embedding

        │

        ▼

Vector Search
```

Only **one embedding** is created.

If that embedding doesn't match some relevant documents well, they're never retrieved.

---

# The Idea Behind MultiQueryRetriever

Instead of searching once...

Search **multiple times** using different versions of the same question.

Example:

Original query

```text
What is RAG?
```

LLM generates

```text
1. Explain Retrieval Augmented Generation.

2. How does RAG work?

3. What is a retrieval pipeline?

4. How do LLMs retrieve external knowledge?

5. Explain knowledge retrieval in LLMs.
```

Now each query searches the vector store.

---

# Architecture

```text
                 User Query
                      │
                      ▼
                  LLM Creates
                Multiple Queries
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Search 1         Search 2        Search 3
      │               │               │
      └───────────────┼───────────────┘
                      ▼
           Merge & Remove Duplicates
                      │
                      ▼
           Final Relevant Documents
```

Notice...

The LLM is **not answering the question.**

It is only rewriting the question.

---

# Example

Database

```text
Doc1:
Retrieval-Augmented Generation...

Doc2:
External Knowledge Retrieval...

Doc3:
Vector Databases...

Doc4:
Prompt Engineering...
```

User asks

```text
How does RAG work?
```

Normal Retriever

```text
↓

Finds only

Doc1
```

---

MultiQueryRetriever

LLM generates

```text
Explain Retrieval-Augmented Generation.

Knowledge Retrieval in LLMs.

Context Injection.

External Memory.
```

Now retrieval becomes

```text
Doc1

Doc2

Doc3
```

Way better context.

---

# Why is this useful?

Because **humans ask questions in many different ways.**

Example

```text
How do I lose weight?
```

Could also mean

```text
Fat loss tips

Weight reduction

Burn calories

Dieting

Healthy eating

Exercise for weight loss
```

A single embedding may not capture every nuance.

---

# How LangChain Builds It

Suppose you already have

```python
retriever = vectorstore.as_retriever()
```

Now

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
```

Create

```python
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=model
)
```

That's literally it.

Internally it becomes

```text
VectorStoreRetriever

↓

MultiQueryRetriever
```

---

# Usage

Exactly like every retriever.

```python
docs = multi_retriever.invoke(
    "Explain RAG"
)
```

No difference.

That's because everything follows the **Retriever interface**.

---

# Under the Hood

Suppose

```python
query = "Explain RAG"
```

LLM does

```text
↓

Generate

5 alternative queries
```

Then

```text
Query 1

↓

Retriever

↓

Docs
```

Again

```text
Query 2

↓

Retriever

↓

Docs
```

Again...

Until all queries finish.

Then

```text
Merge

↓

Remove duplicates

↓

Return
```

---

# Why not just increase `k`?

Excellent interview question.

Suppose

```python
k=20
```

You're still searching with

```text
ONE query
```

If the wording of that one query is poor, you'll retrieve **20 mediocre results**.

MultiQueryRetriever instead improves the **search itself** by reformulating the question.

---

# Benefits

✅ Better Recall

Finds more relevant documents.

---

✅ Different Terminology

Handles synonyms.

---

✅ Better RAG

Provides richer context.

---

✅ Handles Ambiguous Questions

Much better than plain similarity search.

---

# Downsides

Every retrieval requires the LLM.

Instead of

```text
User

↓

Retriever
```

it becomes

```text
User

↓

LLM

↓

Retriever
```

So

* More latency
* More API cost

---

# Real-world Usage

It's commonly used in:

* Research assistants
* Medical RAG
* Legal RAG
* Academic search
* Enterprise knowledge bases

Basically anywhere **recall** is more important than speed.

---

# Complete Flow

```text
User Question
      │
      ▼
MultiQueryRetriever
      │
      ▼
LLM Generates
Multiple Search Queries
      │
      ▼
VectorStoreRetriever
      │
      ▼
Retrieve Documents
      │
      ▼
Merge Results
      │
      ▼
Remove Duplicates
      │
      ▼
Return Final Documents
      │
      ▼
LLM Generates Answer
```

---

# Code Example

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.retrievers.multi_query import MultiQueryRetriever

# Embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector Store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

# Base Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# Multi Query Retriever
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

# Retrieve documents
docs = multi_retriever.invoke(
    "Explain Retrieval-Augmented Generation"
)

for doc in docs:
    print(doc.page_content)
```

---

## 🧠 Interview Question

> **When would you choose `MultiQueryRetriever` over a standard `VectorStoreRetriever`?**

A strong answer would be:

> *I'd use `MultiQueryRetriever` when recall is critical. Instead of relying on a single user query, it uses an LLM to generate multiple semantically different versions of the query, retrieves documents for each, merges the results, and removes duplicates. This helps find relevant documents that use different terminology or phrasing, improving the context provided to the LLM at the cost of additional latency and API usage.*
