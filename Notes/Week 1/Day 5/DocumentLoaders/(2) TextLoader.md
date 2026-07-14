LET'S GOOOO!! 🚀🔥

We'll start with the simplest and most fundamental loader:

# 📄 TextLoader

If you understand `TextLoader`, then learning `PDFLoader`, `CSVLoader`, `WebBaseLoader`, etc., becomes much easier because **they all follow nearly the same interface.**

---

# Why TextLoader?

Imagine you have a file called:

```
ai_notes.txt
```

Contents:

```text
Artificial Intelligence is the simulation of human intelligence.

Machine Learning is a subset of AI.

Deep Learning is a subset of Machine Learning.
```

Can LangChain directly use this file?

❌ No.

The LLM only understands text that is passed to it.

So we need something that:

```
ai_notes.txt

↓

Read the file

↓

Extract the text

↓

Create a Document object
```

That is exactly what `TextLoader` does.

---

# What is TextLoader?

> **TextLoader reads a plain text (.txt) file and converts it into one or more LangChain `Document` objects.**

---

# Installation

Usually it's already installed with LangChain Community.

```bash
pip install langchain-community
```

Import:

```python
from langchain_community.document_loaders import TextLoader
```

---

# Your First Example

Suppose we have

```
notes.txt
```

Contents:

```text
Artificial Intelligence is changing the world.

Machine Learning helps computers learn from data.
```

Code

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("notes.txt")

documents = loader.load()

print(documents)
```

Output

```python
[
    Document(
        page_content='Artificial Intelligence is changing the world.\nMachine Learning helps computers learn from data.',
        metadata={
            'source': 'notes.txt'
        }
    )
]
```

Notice something?

It returned

```
A LIST
```

not a single document.

---

# Why a List?

You might wonder:

> "There's only one file. Why does `load()` return a list?"

Excellent question.

Because **LangChain wants every loader to have a consistent interface.**

Some loaders naturally produce multiple documents.

For example:

PDF

```
Page 1

↓

Document

Page 2

↓

Document

Page 3

↓

Document
```

Instead of changing the return type depending on the loader,

LangChain always returns

```python
List[Document]
```

Even if there is only one document.

---

# Accessing the First Document

```python
doc = documents[0]

print(doc)
```

---

# Reading the Text

```python
print(doc.page_content)
```

Output

```text
Artificial Intelligence is changing the world.

Machine Learning helps computers learn from data.
```

---

# Reading Metadata

```python
print(doc.metadata)
```

Output

```python
{
    "source":"notes.txt"
}
```

---

# Visual

```
notes.txt

↓

TextLoader

↓

[
 Document
]

↓

Document

├── page_content
│
└── metadata
```

---

# Example

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("notes.txt")

documents = loader.load()

doc = documents[0]

print(doc.page_content)

print()

print(doc.metadata)
```

---

# Understanding the Document Object

Think of a `Document` like this:

```python
Document(

page_content="AI is changing the world.",

metadata={

"source":"notes.txt"

}

)
```

Only two important things exist.

```
Document

│

├── page_content

└── metadata
```

---

# Another Example

Suppose

```
student.txt
```

contains

```text
Name : Imran

University : UCP

Semester : 4

Department : BSCS
```

Code

```python
loader = TextLoader("student.txt")

docs = loader.load()

print(docs[0].page_content)
```

Output

```text
Name : Imran

University : UCP

Semester : 4

Department : BSCS
```

---

# Common Methods

The first method you'll use most is:

## `load()`

Reads the entire file immediately.

```python
docs = loader.load()
```

Memory

```
Entire File

↓

RAM

↓

Documents
```

Good for

* Small files
* Most projects

---

## `lazy_load()`

Instead of loading everything immediately,

it loads documents one by one.

```python
loader = TextLoader("notes.txt")

for doc in loader.lazy_load():

    print(doc.page_content)
```

Think of it like streaming.

```
Huge File

↓

One Document

↓

Next Document

↓

Next Document

↓

Next Document
```

Useful for very large datasets or when processing documents incrementally.

---

# Encoding

Sometimes you'll get

```
UnicodeDecodeError
```

because the loader doesn't know the file encoding.

Specify it manually:

```python
loader = TextLoader(

    "notes.txt",

    encoding="utf-8"

)
```

Other common encodings include:

```
utf-8
latin-1
cp1252
```

---

# Complete Flow

```
notes.txt

↓

TextLoader

↓

Document

↓

page_content

↓

TextSplitter

↓

Embeddings

↓

Vector Database

↓

Retriever

↓

LLM
```

---

# Real-Life Analogy

Imagine a librarian.

You hand them a book.

```
Book

↓

Librarian

↓

Book Card
```

The card contains

```
Title

Author

Pages

Content
```

The librarian didn't explain the book.

They simply organized it into a standard format.

`TextLoader` works exactly like that.

---

# Summary

| Concept        | Description                                      |
| -------------- | ------------------------------------------------ |
| `TextLoader`   | Reads a `.txt` file                              |
| `load()`       | Loads all documents at once                      |
| `lazy_load()`  | Loads documents one at a time                    |
| Return Type    | `List[Document]`                                 |
| `page_content` | The actual text                                  |
| `metadata`     | Extra information like source, page number, etc. |

---

## 🎯 Key Takeaway

The most important thing to remember isn't `TextLoader` itself—it's the **`Document` object**.

Every loader you'll learn next (`PyPDFLoader`, `CSVLoader`, `WebBaseLoader`, `DirectoryLoader`, etc.) ultimately gives you the same thing:

```python
List[Document]
```

The only difference is **where the data comes from**. Once it's loaded, the rest of the LangChain pipeline treats it the same way. That's one of the biggest design strengths of LangChain.
