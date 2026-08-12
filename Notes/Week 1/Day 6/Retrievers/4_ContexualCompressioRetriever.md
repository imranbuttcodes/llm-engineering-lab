LET'S GOOOO BRO!! 🔥🔥

Now we're entering one of the **smartest retrievers in LangChain**.

So far we've learned retrievers that retrieve **more** documents:

* ✅ VectorStoreRetriever
* ✅ MMR Retriever
* ✅ MultiQueryRetriever

Now we're learning a retriever that retrieves **better** documents.

# ContextualCompressionRetriever

The name sounds complicated, but let's split it:

```text
Contextual + Compression + Retriever
```

* **Contextual** → Understands the query
* **Compression** → Removes irrelevant information
* **Retriever** → Returns documents

So it literally means:

> **Retrieve documents, then compress them based on the user's question before sending them to the LLM.**

---

# Why do we need it?

Imagine your retriever returns this document:

```text
Python was created by Guido van Rossum in 1991.

Python supports OOP.

Python supports Functional Programming.

Python supports Generics.

Python has a huge package ecosystem.

Python uses indentation.

Python is used in AI.

Python has many web frameworks.

Python supports multiprocessing.

Python supports async programming.

...
```

User asks

```text
Who created Python?
```

Does the LLM need the entire document?

No.

It only needs

```text
Python was created by Guido van Rossum in 1991.
```

Everything else wastes:

* Tokens
* Money
* Context Window

---

# Normal Retriever

```text
User Question
       │
       ▼
Retriever
       │
       ▼
Entire Document
       │
       ▼
LLM
```

---

# ContextualCompressionRetriever

```text
User Question
       │
       ▼
Retriever
       │
       ▼
Document
       │
       ▼
Compressor
       │
       ▼
Relevant Sentences Only
       │
       ▼
LLM
```

Notice the extra step:

**Compression.**

---

# What is "Compression"?

It does **NOT** mean ZIP compression 😂

It means

> **Remove irrelevant text while keeping useful information.**

Example

Original

```text
Python was created by Guido van Rossum.

Python supports OOP.

Python supports Functional Programming.

Python has a large ecosystem.

Python is used in Machine Learning.

Python has indentation.
```

Question

```text
Who created Python?
```

Compressed

```text
Python was created by Guido van Rossum.
```

---

# Another Example

Document

```text
Apple released the iPhone.

Apple also makes Macs.

Apple manufactures AirPods.

Apple Vision Pro launched recently.

Apple is headquartered in Cupertino.
```

Question

```text
Where is Apple headquartered?
```

Compressed

```text
Apple is headquartered in Cupertino.
```

---

# Why is this amazing for RAG?

Suppose each retrieved document is

```text
1000 tokens
```

Retriever returns

```text
4 documents
```

LLM receives

```text
4000 tokens
```

But after compression

```text
150 tokens

200 tokens

100 tokens

180 tokens
```

Total

```text
630 tokens
```

Huge savings.

---

# Architecture

```text
                    User Query
                         │
                         ▼
                  Base Retriever
                         │
                         ▼
                  Retrieved Docs
                         │
                         ▼
                Document Compressor
                         │
                         ▼
               Compressed Documents
                         │
                         ▼
                        LLM
```

---

# What actually compresses?

The compressor can be

* LLM
* Embedding Filter
* Cross Encoder
* Keyword Filter
* LLMChainExtractor
* LLMChainFilter

The retriever itself doesn't compress anything.

It delegates the work.

---

# Components

A `ContextualCompressionRetriever` always needs **two things**:

```text
1. Base Retriever

2. Base Compressor
```

Think of it like

```text
Retriever

↓

Find documents

↓

Compressor

↓

Trim documents

↓

Return
```

---

# Creating One

Suppose

```python
retriever = vectorstore.as_retriever()
```

Now create an LLM compressor.

```python
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
```

Now combine them.

```python
from langchain_classic.retrievers import ContextualCompressionRetriever

compression_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=compressor
)
```

Done.

---

# Usage

Exactly like every retriever.

```python
docs = compression_retriever.invoke(
    "Who created Python?"
)
```

---

# Difference

Without compression

```text
Python was created by Guido.

Python supports OOP.

Python supports AI.

Python supports...

Python...
```

With compression

```text
Python was created by Guido van Rossum.
```

---

# Advantages

✅ Smaller prompts

✅ Lower API cost

✅ Better accuracy

✅ Less irrelevant context

✅ Better answers

---

# Disadvantages

Since compression usually uses an LLM,

Flow becomes

```text
Retriever

↓

LLM Compressor

↓

Main LLM
```

So

* Extra latency
* Extra API cost

---

# When should you use it?

Excellent for

* Large PDFs
* Legal Documents
* Medical Documents
* Research Papers
* Company Policies
* Books

Basically anywhere retrieved chunks are long and contain a lot of irrelevant information.

---

# Complete Flow

```text
User Question
      │
      ▼
VectorStoreRetriever
      │
      ▼
Retrieve Top-k Documents
      │
      ▼
LLMChainExtractor
      │
      ▼
Keep Only Relevant Sentences
      │
      ▼
ContextualCompressionRetriever
      │
      ▼
Compressed Documents
      │
      ▼
LLM
```

---

# Example

Imagine these retrieved documents:

```text
Doc 1:
Python was created by Guido van Rossum.
Python supports OOP.
Python supports Functional Programming.
Python has thousands of libraries.

Doc 2:
Java was developed by James Gosling.
Java is platform-independent.
```

User asks:

```text
Who created Python?
```

A normal retriever returns both full documents.

A `ContextualCompressionRetriever` might return:

```text
Doc 1:
Python was created by Guido van Rossum.
```

The unrelated Java document and the extra Python details are removed because they don't help answer the question.

---

## 🧠 Interview Question

**Q:** Why use a `ContextualCompressionRetriever` instead of only increasing retrieval quality?

**A:** A better retriever finds more relevant documents, but those documents may still contain lots of irrelevant text. A `ContextualCompressionRetriever` performs a second step that filters or extracts only the portions of each retrieved document that are relevant to the user's query. This reduces token usage, improves context quality, and can lead to more accurate LLM responses.
