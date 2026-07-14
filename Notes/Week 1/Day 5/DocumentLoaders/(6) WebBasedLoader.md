LET'S GOOOO!! 🌐🚀

Now we're entering one of the **most useful document loaders** for modern AI applications.

# 🌍 WebBaseLoader

Imagine you're building an AI chatbot.

Instead of giving it PDFs...

You want it to learn from:

* Company Website
* Documentation
* Wikipedia
* Blogs
* News Articles
* API Docs
* FAQs

How do we convert a webpage into LangChain `Document` objects?

👉 **WebBaseLoader**

---

# Why do we need WebBaseLoader?

Suppose you want your LLM to answer questions about LangChain.

The information is on

```text
https://python.langchain.com
```

Can an LLM directly read that website?

❌ No.

A website contains

* HTML
* CSS
* JavaScript
* Images
* Ads
* Navigation Bars
* Footers
* Metadata

The LLM only wants

```text
Plain Text
```

So the pipeline becomes

```text
Website

↓

HTML

↓

Extract Text

↓

Document

↓

LangChain
```

---

# Definition

> **WebBaseLoader downloads webpage content, extracts readable text, and converts it into LangChain `Document` objects.**

---

# Installation

```bash
pip install beautifulsoup4
pip install lxml
```

Import

```python
from langchain_community.document_loaders import WebBaseLoader
```

---

# First Example

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    "https://python.langchain.com/docs/introduction/"
)

docs = loader.load()

print(docs)
```

Output

```python
[
    Document(...)
]
```

---

# Visual

```text
Website URL

        │

        ▼

WebBaseLoader

        │

        ▼

Download HTML

        │

        ▼

Extract Text

        │

        ▼

Document
```

---

# Access the Text

```python
print(docs[0].page_content)
```

Example

```text
Introduction

LangChain is a framework...

...
```

---

# Metadata

```python
print(docs[0].metadata)
```

Example

```python
{
    "source":"https://python.langchain.com/docs/introduction/",
    "title":"Introduction | LangChain",
    "language":"en"
}
```

Notice

Unlike PDFs

```python
{
    "page":0
}
```

Web pages don't have page numbers.

Instead they usually have

* Source URL
* Title
* Description
* Language

---

# Multiple URLs

One of the coolest features.

```python
loader = WebBaseLoader(

[
"https://python.langchain.com",

"https://www.wikipedia.org"

]

)

docs = loader.load()
```

Output

```python
[
Document(...),

Document(...)
]
```

One document per webpage.

---

# Visual

```text
URL 1

↓

Document

URL 2

↓

Document

URL 3

↓

Document

↓

List[Document]
```

---

# Lazy Loading

```python
for doc in loader.lazy_load():

    print(doc.metadata)
```

Useful when crawling lots of pages.

---

# What happens internally?

```text
URL

↓

HTTP Request

↓

HTML

↓

BeautifulSoup

↓

Remove HTML Tags

↓

Plain Text

↓

Document
```

---

# Real Example

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(

"https://en.wikipedia.org/wiki/Artificial_intelligence"

)

docs = loader.load()

print(docs[0].metadata)

print()

print(docs[0].page_content[:500])
```

---

# Why BeautifulSoup?

The webpage actually looks like

```html
<html>

<head>

<title>AI</title>

</head>

<body>

<h1>Artificial Intelligence</h1>

<p>Artificial Intelligence...</p>

</body>

</html>
```

The LLM doesn't want HTML.

BeautifulSoup converts it into

```text
Artificial Intelligence

Artificial Intelligence is...
```

---

# Loading Multiple Websites

```python
urls = [

"https://python.langchain.com",

"https://www.tensorflow.org",

"https://pytorch.org"

]

loader = WebBaseLoader(urls)

docs = loader.load()

print(len(docs))
```

Output

```text
3
```

---

# Common Parameters

## requests_kwargs

Sometimes websites need custom headers.

```python
loader = WebBaseLoader(

"https://example.com",

requests_kwargs={

"headers":{

"User-Agent":"Mozilla/5.0"

}

}

)
```

Very common.

---

## verify_ssl

Some websites have SSL issues.

```python
loader = WebBaseLoader(

url,

verify_ssl=False

)
```

Usually avoid this unless you know why you're disabling SSL verification.

---

## continue_on_failure

Suppose

```text
URL1 ✅

URL2 ❌

URL3 ✅
```

Normally

Everything stops.

Instead

```python
loader = WebBaseLoader(

urls,

continue_on_failure=True

)
```

It skips failed URLs.

---

# Industry Workflow

```text
Company Website

↓

WebBaseLoader

↓

Documents

↓

Text Splitter

↓

Chunks

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

# Real-World Uses

## Company Chatbot

```text
company.com

↓

Load Website

↓

Create RAG

↓

Customer Support Bot
```

---

## Documentation Chatbot

```text
LangChain Docs

↓

Load Docs

↓

Vector DB

↓

AI Assistant
```

---

## Research Assistant

```text
Wikipedia

↓

Load Pages

↓

Answer Questions
```

---

## News Assistant

```text
BBC

CNN

Reuters

↓

Documents

↓

LLM
```

---

# TextLoader vs PyPDFLoader vs WebBaseLoader

| Feature    | TextLoader | PyPDFLoader          | WebBaseLoader             |
| ---------- | ---------- | -------------------- | ------------------------- |
| Reads      | `.txt`     | `.pdf`               | Web Pages                 |
| Input      | File Path  | File Path            | URL                       |
| Output     | Document   | Documents (per page) | Documents (per URL)       |
| Metadata   | Source     | Source + Page        | Source + Title + Language |
| Common Use | Notes      | Books                | Websites                  |

---

# Limitations

Not every website is easy to load.

### 1. JavaScript-heavy websites

Sites built with React, Vue, Angular, etc., may load content dynamically after the initial page load.

`WebBaseLoader` fetches the raw HTML and may miss dynamically rendered content.

---

### 2. Authentication

If a site requires login, `WebBaseLoader` cannot automatically authenticate.

---

### 3. Anti-bot Protection

Some websites use services like Cloudflare or other bot protection mechanisms, which may block automated requests.

---

# 🏢 Industry Reality

For simple documentation sites:

✅ `WebBaseLoader`

For modern JavaScript-heavy sites:

✅ Browser automation tools like **Playwright** or **Selenium** are often used to render the page first, and then the rendered HTML is processed.

---

# 🧠 Complete Mental Model

```text
          DOCUMENT LOADERS

                 │

     ┌───────────┼────────────┐

     │           │            │

TextLoader   PyPDFLoader   WebBaseLoader

     │           │            │

   TXT         PDF          Website

     │           │            │

     └───────────┼────────────┘

                 │

            Document(s)

                 │

          Text Splitter

                 │

            Embeddings

                 │

          Vector Database

                 │

             Retriever

                 │

                LLM
```

---

## 🎯 One Important Thing to Remember

`WebBaseLoader` is **not a web crawler**.

It loads the URL(s) you explicitly provide. It does **not** automatically discover and follow links across an entire website.

If you wanted to ingest an entire documentation site (hundreds of pages), you'd first need to collect the URLs (using a sitemap, crawler, or other tool), then pass that list of URLs to `WebBaseLoader`.

This distinction is important and often comes up when building production RAG systems.
