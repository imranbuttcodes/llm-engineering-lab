LET'S GOOOOO!! 🚀🔥

Welcome to one of the most important topics in LangChain.

Until now, we've been giving the LLM information manually:

```python
model.invoke("What is AI?")
```

or

```python
prompt | model | parser
```

But in real-world AI applications, the data doesn't come from you typing it.

It comes from:

* 📄 PDF files
* 📃 Word documents
* 📑 Text files
* 🌐 Websites
* 📰 Blogs
* 🗂️ CSV files
* 📊 Excel sheets
* 🗄️ Databases
* 📧 Emails
* ☁️ Google Drive
* 🐙 GitHub repositories
* 📝 Notion pages
* 💬 Slack/Discord messages
* 🎥 YouTube transcripts
* ...

So the question becomes:

> **How do we get all this data into LangChain?**

The answer is...

# 📂 Document Loaders

---

# High-Level Overview

```text
                External Data Sources
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
   PDF                Website             Database
     │                   │                   │
     └───────────────────┼───────────────────┘
                         │
                  Document Loader
                         │
                         ▼
             LangChain Document Objects
                         │
                         ▼
                Text Splitter
                         │
                         ▼
                  Embeddings
                         │
                         ▼
                 Vector Database
                         │
                         ▼
                     Retriever
                         │
                         ▼
                        LLM
```

Notice something?

This is the **beginning of every RAG pipeline.**

---

# Why do we need Document Loaders?

Suppose you have this PDF:

```
Machine Learning Notes.pdf
```

Can the LLM read it directly?

❌ No.

It only understands text.

So we need something that

```
PDF
   ↓
Extract Text
   ↓
Convert into LangChain Document
```

That "something" is a **Document Loader**.

---

# Definition

> **A Document Loader loads data from an external source and converts it into LangChain's standard `Document` objects.**

Think of it as a translator.

```
Real World File

↓

Document Loader

↓

LangChain Document
```

---

# What is a Document?

In LangChain, a document is **not** just text.

It has two parts.

```python
Document(
    page_content="This is AI.",

    metadata={
        "source":"notes.pdf",
        "page":5
    }
)
```

So every document contains

```
Document
│
├── page_content
│
└── metadata
```

---

## page_content

The actual text.

Example

```text
Artificial Intelligence is...
```

---

## metadata

Extra information.

Example

```python
{
    "source":"AI.pdf",

    "page":10
}
```

Metadata helps later during retrieval.

---

# Visual

```text
PDF

↓

Document Loader

↓

Document

├── page_content
│      "Artificial Intelligence..."
│
└── metadata
       source="AI.pdf"
       page=10
```

---

# Types of Document Loaders

There are **dozens** of loaders.

The most common ones are:

```
Document Loaders
│
├── TextLoader
├── PyPDFLoader
├── CSVLoader
├── UnstructuredExcelLoader
├── JSONLoader
├── DirectoryLoader
├── WebBaseLoader
├── UnstructuredHTMLLoader
├── YouTubeLoader
├── NotionLoader
├── GitLoader
├── ConfluenceLoader
├── NotionDBLoader
├── SeleniumURLLoader
├── WikipediaLoader
├── ...
```

LangChain supports **100+ document loaders**.

---

# Think of them like USB adapters

Imagine you have different devices.

```
Phone

Laptop

Camera

Printer
```

Each has a different connector.

Instead of changing the computer,

you use the correct adapter.

Document Loaders work exactly like adapters.

```
PDF

↓

PyPDFLoader

↓

Document
```

```
Website

↓

WebBaseLoader

↓

Document
```

```
CSV

↓

CSVLoader

↓

Document
```

Everything becomes the same format.

---

# Where do they fit?

Complete AI pipeline

```
User Data
     │
     ▼
Document Loader
     │
     ▼
Document
     │
     ▼
Text Splitter
     │
     ▼
Chunks
     │
     ▼
Embeddings
     │
     ▼
Vector Database
     │
     ▼
Retriever
     │
     ▼
Prompt
     │
     ▼
LLM
```

---

# Learning Roadmap

We'll cover these one by one:

```
Document Loaders
│
├── 📄 TextLoader
│
├── 📄 PyPDFLoader
│
├── 📁 DirectoryLoader
│
├── 🌐 WebBaseLoader
│
├── 📊 CSVLoader
│
├── 📝 JSONLoader
│
└── (Optional)
    ├── YouTubeLoader
    ├── GitLoader
    └── NotionLoader
```

---

# Day 5 Progress

Here's where you are now:

```
Day 5
│
├── ✅ Why Runnables?
├── ✅ Runnable Categories
├── ✅ RunnableLambda
├── ✅ RunnablePassthrough
├── ✅ RunnableAssign
├── ✅ RunnablePick
│
└── 🔥 Document Loaders
      ↑ Starting now
```

---

## 💡 Before we write any code...

Here's one important concept to keep in mind:

> **A Document Loader does not make your AI "understand" the document. It only reads and converts it into LangChain `Document` objects.**

The *understanding* happens much later through:

1. **Text Splitters** (break the document into chunks),
2. **Embeddings** (convert chunks into vectors),
3. **Vector Stores** (store those vectors),
4. **Retrievers** (find relevant chunks),
5. **The LLM** (generate the final answer).

So think of a Document Loader as the **ingestion step**—its only job is to bring external data into a format that the rest of the LangChain pipeline can work with.

## 🚀 Next up

We'll start with the simplest loader: **`TextLoader`**, because it introduces the `Document` object and the common API (`load()`, `lazy_load()`, etc.) that most other loaders follow.
