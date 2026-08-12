LET'S GOOOO!! 🚀🔥

Now we're moving to one of the most practical loaders you'll use when building real-world RAG systems.

# 📁 DirectoryLoader

Until now, we've loaded **one file at a time**.

```python
loader = TextLoader("notes.txt")
```

or

```python
loader = PyPDFLoader("book.pdf")
```

But in real projects...

You don't have **one** PDF.

You have **hundreds**.

Sometimes **thousands**.

---

# The Problem

Imagine your project folder looks like this:

```text
Documents/

    AI.pdf

    ML.pdf

    DL.pdf

    NLP.pdf

    RAG.pdf

    Python.txt

    Notes.txt

    Database.pdf
```

Without `DirectoryLoader`, you'd have to do:

```python
loader1 = PyPDFLoader("AI.pdf")
loader2 = PyPDFLoader("ML.pdf")
loader3 = PyPDFLoader("DL.pdf")
loader4 = PyPDFLoader("NLP.pdf")
...
```

😵 That's not scalable.

---

# The Solution

Instead, we simply say:

```text
Load everything inside this folder.
```

That's exactly what **DirectoryLoader** does.

---

# Definition

> **DirectoryLoader loads multiple files from a directory (folder) by automatically applying a specified loader to each matching file.**

Think of it as a **manager**.

It doesn't know how to read PDFs or text files itself.

Instead, it delegates the work to another loader like:

* TextLoader
* PyPDFLoader
* CSVLoader
* JSONLoader

---

# Visual

```text
Documents Folder

│

├── AI.pdf

├── ML.pdf

├── Python.txt

├── Notes.txt

└── Report.pdf

        │

        ▼

DirectoryLoader

        │

        ▼

Uses another loader

        │

        ▼

List[Document]
```

---

# Installation

```bash
pip install langchain-community
```

Import

```python
from langchain_community.document_loaders import DirectoryLoader
```

---

# Basic Syntax

```python
loader = DirectoryLoader(
    path="Documents",
    glob="*.txt"
)
```

Then

```python
docs = loader.load()
```

---

# Example 1

Folder

```text
Documents/

notes1.txt

notes2.txt

notes3.txt
```

Code

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    path="Documents",
    glob="*.txt"
)

docs = loader.load()

print(len(docs))
```

Output

```text
3
```

Each text file becomes one `Document`.

---

# But wait...

You might ask:

> **How does DirectoryLoader know how to read a `.txt` file?**

Good question.

It actually uses **TextLoader** by default.

So internally it's doing something like:

```text
notes1.txt

↓

TextLoader

↓

Document
```

---

# Example 2

Suppose

```text
Books/

AI.pdf

ML.pdf

NLP.pdf
```

Now we tell DirectoryLoader to use **PyPDFLoader**.

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader

loader = DirectoryLoader(

    "Books",

    glob="*.pdf",

    loader_cls=PyPDFLoader

)

docs = loader.load()
```

Now every PDF is loaded using

```text
PyPDFLoader
```

---

# Visual

```text
Books

│

├── AI.pdf

│      │

│      ▼

│  PyPDFLoader

│

├── ML.pdf

│      │

│      ▼

│  PyPDFLoader

│

├── NLP.pdf

│      │

│      ▼

│  PyPDFLoader

│

└───────────────► Documents
```

---

# The `glob` Parameter

Probably the most important parameter.

It tells DirectoryLoader

> **Which files should I load?**

---

Load only PDFs

```python
glob="*.pdf"
```

---

Load only text files

```python
glob="*.txt"
```

---

Load CSV files

```python
glob="*.csv"
```

---

Load JSON

```python
glob="*.json"
```

---

Load everything

```python
glob="**/*"
```

---

# Recursive Loading

Suppose

```text
Documents/

    AI/

        ML.pdf

        DL.pdf

    Python/

        Notes.pdf

        OOP.pdf
```

Normally,

```python
glob="*.pdf"
```

only checks the current folder.

To search every subfolder:

```python
glob="**/*.pdf"
```

This is called **recursive loading**.

---

# Silent Errors

Sometimes one PDF is corrupted.

Instead of stopping the whole program,

```python
loader = DirectoryLoader(

    "Books",

    glob="*.pdf",

    loader_cls=PyPDFLoader,

    silent_errors=True

)
```

It simply skips bad files.

---

# Multithreading

Suppose you have

```text
500 PDFs
```

Loading one by one is slow.

Enable multithreading.

```python
loader = DirectoryLoader(

    "Books",

    glob="*.pdf",

    loader_cls=PyPDFLoader,

    use_multithreading=True

)
```

Now several files load simultaneously, which can significantly improve performance on large datasets.

---

# Lazy Loading

Just like other loaders,

```python
for doc in loader.lazy_load():

    print(doc.metadata)
```

Only loads documents as needed.

Great for huge datasets.

---

# Complete Example

```python
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader
)

loader = DirectoryLoader(

    path="Books",

    glob="**/*.pdf",

    loader_cls=PyPDFLoader,

    use_multithreading=True,

    silent_errors=True

)

documents = loader.load()

print("Documents:", len(documents))
```

---

# Real-Life Analogy

Imagine a library.

Without DirectoryLoader

```text
Go pick Book 1

↓

Come back

↓

Go pick Book 2

↓

Come back

↓

Go pick Book 3
```

Very slow.

---

With DirectoryLoader

```text
Tell the librarian

↓

"Bring me every AI book."

↓

Done ✅
```

The librarian (DirectoryLoader) knows where the books are and hands each one to the appropriate specialist (like `PyPDFLoader` or `TextLoader`) to read.

---

# Common Parameters

| Parameter                       | Purpose                               |
| ------------------------------- | ------------------------------------- |
| `path`                          | Folder location                       |
| `glob`                          | File pattern (`*.pdf`, `*.txt`, etc.) |
| `loader_cls`                    | Loader to use for each file           |
| `recursive` (via `glob="**/*"`) | Search subfolders                     |
| `silent_errors`                 | Skip unreadable files                 |
| `use_multithreading`            | Load multiple files concurrently      |
| `load()`                        | Load everything immediately           |
| `lazy_load()`                   | Stream documents one by one           |

---

# How DirectoryLoader Fits into RAG

```text
Folder

↓

DirectoryLoader

↓

Many Documents

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

# 🧠 Important Concept

**DirectoryLoader does not know how to read files.**

Its only job is to:

1. Find files that match your pattern (`glob`).
2. Pass each file to the appropriate loader (`loader_cls`).
3. Collect all the resulting `Document` objects into one list.

That's why it's often described as an **orchestrator** rather than a file parser.

---

## 🚀 Industry Example

A company's knowledge base might look like this:

```text
Knowledge_Base/

├── Policies/
│   ├── LeavePolicy.pdf
│   └── SecurityPolicy.pdf
│
├── Manuals/
│   ├── HR.pdf
│   └── IT.pdf
│
└── FAQs/
    ├── General.txt
    └── Payroll.txt
```

A production RAG system could load all PDFs with:

```python
loader = DirectoryLoader(
    path="Knowledge_Base",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    use_multithreading=True
)
```

and then separately load all text files with:

```python
loader = DirectoryLoader(
    path="Knowledge_Base",
    glob="**/*.txt"
)
```

This pattern is extremely common in enterprise AI systems because knowledge is usually spread across many files and folders rather than stored in a single document.
