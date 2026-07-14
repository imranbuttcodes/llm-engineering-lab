LET'S GOOOO!! 🚀🔥

Now we're moving to one of the **most used document loaders in the entire LangChain ecosystem**.

# 📄 PyPDFLoader

If someone builds a RAG application, there's a **90% chance they're loading PDFs**.

Why?

Because companies store knowledge in PDFs:

* 📚 Research Papers
* 📖 Books
* 📑 User Manuals
* 📄 Company Policies
* 📊 Annual Reports
* 📜 Legal Contracts
* 🎓 Lecture Notes
* 📘 Documentation

So learning `PyPDFLoader` is essential.

---

# Why do we need PyPDFLoader?

Suppose you have

```text
Machine_Learning.pdf
```

Can LangChain understand this directly?

❌ No.

A PDF is **not plain text**.

It contains:

* Fonts
* Images
* Formatting
* Tables
* Metadata
* Multiple pages

The LLM only wants...

```text
"This is the text..."
```

So we need

```text
PDF

↓

Extract text

↓

Split page by page

↓

Create Documents

↓

LangChain
```

---

# Definition

> **PyPDFLoader extracts text from a PDF and converts each page into a separate LangChain `Document`.**

Unlike `TextLoader`, which usually returns **one document**, `PyPDFLoader` typically returns **one document per page**.

---

# Installation

```bash
pip install pypdf
```

Import

```python
from langchain_community.document_loaders import PyPDFLoader
```

---

# Your First Example

Suppose

```text
AI_Book.pdf
```

contains

```
Page 1
Introduction to AI

Page 2
Machine Learning

Page 3
Deep Learning
```

Code

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("AI_Book.pdf")

documents = loader.load()

print(documents)
```

Output (simplified)

```python
[
    Document(...Page 1...),

    Document(...Page 2...),

    Document(...Page 3...)
]
```

Notice?

Each page becomes a separate `Document`.

---

# Visual

```text
AI_Book.pdf

      │

      ▼

PyPDFLoader

      │

      ▼

Document(Page 1)

Document(Page 2)

Document(Page 3)
```

---

# Accessing a Page

First page

```python
print(documents[0].page_content)
```

Second page

```python
print(documents[1].page_content)
```

Third page

```python
print(documents[2].page_content)
```

Exactly like a Python list.

---

# Metadata

Let's inspect it.

```python
print(documents[0].metadata)
```

Example

```python
{
    "source":"AI_Book.pdf",

    "page":0
}
```

Page numbering starts from **0**.

---

Second page

```python
{
    "source":"AI_Book.pdf",

    "page":1
}
```

---

# Structure

Each page becomes

```python
Document(

page_content="Text of page",

metadata={

"source":"AI_Book.pdf",

"page":0

}

)
```

---

# Example

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("AI_Book.pdf")

docs = loader.load()

for doc in docs:

    print(doc.metadata)

    print(doc.page_content)

    print("-"*40)
```

Output

```text
Page 0
Introduction...

----------------

Page 1
Machine Learning...

----------------

Page 2
Deep Learning...
```

---

# Why page-by-page?

Imagine a 500-page book.

Would you want

```text
One huge document
```

❌ No.

Instead

```text
Page 1

↓

Document

Page 2

↓

Document

...

Page 500

↓

Document
```

Much easier to process.

---

# load()

Loads every page immediately.

```python
loader.load()
```

Returns

```python
List[Document]
```

---

# lazy_load()

Loads pages one by one.

```python
loader = PyPDFLoader("book.pdf")

for page in loader.lazy_load():

    print(page.metadata)
```

Useful for

* Huge books
* Large reports
* Memory-efficient processing

---

# Complete Example

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("ML.pdf")

documents = loader.load()

print("Number of pages:", len(documents))

print()

print(documents[0].page_content)

print()

print(documents[0].metadata)
```

---

# Real-Life Analogy

Imagine a textbook.

```
Book

↓

Open it

↓

Separate every page

↓

Put every page into a folder
```

That's exactly what `PyPDFLoader` does.

Each page becomes its own `Document`.

---

# TextLoader vs PyPDFLoader

| Feature    | TextLoader         | PyPDFLoader             |
| ---------- | ------------------ | ----------------------- |
| Reads      | `.txt`             | `.pdf`                  |
| Output     | Usually 1 Document | One Document per page   |
| Metadata   | Source             | Source + Page Number    |
| Common Use | Notes, logs        | Books, reports, manuals |

---

# Complete Pipeline

```text
PDF

↓

PyPDFLoader

↓

Documents

↓

Text Splitter

↓

Chunks

↓

Embeddings

↓

Vector Store

↓

Retriever

↓

LLM
```

---

# 🔥 One Important Question

You might ask:

> **If each page is already a separate `Document`, why do we still need a `TextSplitter`?**

Excellent question.

Because a single PDF page can still contain **800–2000 words**, which is often too large for embeddings or efficient retrieval.

So the flow becomes:

```text
PDF

↓

PyPDFLoader

↓

Page 1 Document
        │
        ▼
TextSplitter
        │
        ▼
Chunk 1
Chunk 2
Chunk 3

Page 2 Document
        │
        ▼
Chunk 1
Chunk 2
```

So:

* **PyPDFLoader** → splits the PDF into **pages**.
* **TextSplitter** → splits each page into **smaller chunks**.

This two-stage process is the standard approach used in most production RAG systems.

---

## 🚀 Next loaders I'd recommend

Now that you know `TextLoader` and `PyPDFLoader`, the most valuable loaders to learn next are:

1. 📁 `DirectoryLoader` (load many files at once)
2. 🌐 `WebBaseLoader` (load webpages)
3. 📊 `CSVLoader`
4. 📝 `JSONLoader`

These four, along with the two you've already learned, cover a very large percentage of real-world LangChain projects.
