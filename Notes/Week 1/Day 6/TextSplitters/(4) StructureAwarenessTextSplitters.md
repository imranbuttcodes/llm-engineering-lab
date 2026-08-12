Awesome! 🔥 You've now learned the **size-based splitters**. Let's move to the next category.

---

# Structure-Aware Text Splitters

Until now, every splitter we've learned asks:

> **"How big should each chunk be?"**

Now we're asking a different question:

> **"How is this document organized?"**

Instead of preserving **size**, these splitters preserve **structure**.

Imagine you have a Markdown file like this:

```markdown
# Machine Learning

Introduction...

## Supervised Learning

Text...

## Unsupervised Learning

Text...

### PCA

Text...

### K-Means

Text...

# Deep Learning

Text...
```

Would you want this?

```text
Chunk 1
----------------
# Machine Learning

Introduction...

## Supervised Learning

Text...

## Unsuperv
```

😬

Or this?

```text
Chunk 1
----------------
# Machine Learning

Introduction...

----------------

Chunk 2
----------------
## Supervised Learning

Text...

----------------

Chunk 3
----------------
## Unsupervised Learning

Text...

----------------

Chunk 4
----------------
### PCA

Text...

----------------

Chunk 5
----------------
### K-Means

Text...
```

Obviously the second one.

That's exactly what **structure-aware splitters** do.

---

# MarkdownHeaderTextSplitter

## Why?

Suppose you're building an AI chatbot over documentation.

Examples:

* LangChain Docs
* FastAPI Docs
* React Docs
* Python Docs
* README.md
* GitHub Wikis

These documents are already well organized using headings.

Instead of cutting by characters...

We split by headings.

---

## Example Markdown

```markdown
# Python

Python is a programming language.

## Variables

Variables store values.

## Loops

Loops repeat code.

### For Loop

for i in range(10):

### While Loop

while True:

# Machine Learning

ML is...
```

---

## Without Markdown Splitter

```text
Chunk 1

Python is a programming language...

Variables store values...

Loops repeat...

for i...
```

No hierarchy.

---

## With Markdown Splitter

```text
Chunk 1

Header:
Python

Content:
Python is a programming language.
```

---

```text
Chunk 2

Header:
Variables

Content:
Variables store values.
```

---

```text
Chunk 3

Header:
Loops

Content:
Loops repeat...
```

---

```text
Chunk 4

Header:
For Loop

Content:
for i in range(10)
```

Beautiful.

---

# Constructor

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)
```

---

# Example

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# Python

Python is a programming language.

## Variables

Variables store values.

## Loops

Loops execute code repeatedly.

### For Loop

Example of for loop.
"""

headers = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers
)

docs = splitter.split_text(markdown_text)

for doc in docs:
    print("=" * 50)
    print(doc.page_content)
    print(doc.metadata)
```

---

## Output

```text
==================================================

Python is a programming language.

{'Header 1': 'Python'}

==================================================

Variables store values.

{
'Header 1': 'Python',
'Header 2': 'Variables'
}

==================================================

Loops execute code repeatedly.

{
'Header 1': 'Python',
'Header 2': 'Loops'
}

==================================================

Example of for loop.

{
'Header 1': 'Python',
'Header 2': 'Loops',
'Header 3': 'For Loop'
}
```

Notice something amazing.

The metadata stores the document hierarchy.

Instead of

```python
metadata = {
    "page": 4
}
```

you get

```python
metadata = {
    "Header 1": "Python",
    "Header 2": "Loops",
    "Header 3": "For Loop"
}
```

That makes retrieval much more meaningful.

---

# Why is this useful?

Suppose the user asks:

> Explain For Loops.

The retriever immediately knows

```text
Python

↓

Loops

↓

For Loop
```

instead of searching random text.

---

# HTMLHeaderTextSplitter

Exactly the same idea...

but for HTML.

Instead of

```markdown
#
##
###
```

it understands

```html
<h1>

<h2>

<h3>

<h4>
```

Perfect for:

* Websites
* Documentation
* Blogs
* HTML pages

---

Example

```html
<h1>Machine Learning</h1>

<p>...</p>

<h2>PCA</h2>

<p>...</p>
```

becomes

```text
Document

Header:
Machine Learning

Content:
...

----------------

Document

Header:
PCA

Content:
...
```

---

# JSON Splitter

Suppose your document is

```json
{
  "employee": {
    "name": "Imran",
    "department": {
      "name": "AI",
      "projects": [
        ...
      ]
    }
  }
}
```

A normal splitter would destroy the structure.

A JSON splitter preserves it.

---

# Code Splitters

There are also language-aware splitters.

Example:

```python
class Student:

    def login():

    def logout():

class Teacher:

    def assign():
```

Instead of cutting randomly,

they split around:

* Classes
* Functions
* Methods

This is especially useful for AI coding assistants.

---

# Comparison

| Splitter       | Splits By                  | Best For                  |
| -------------- | -------------------------- | ------------------------- |
| Character      | Characters                 | Learning, simple text     |
| Recursive      | Paragraphs → Lines → Words | PDFs, books, articles ⭐   |
| Token          | Tokens                     | Strict LLM context limits |
| MarkdownHeader | Markdown headings          | README, docs, GitHub      |
| HTMLHeader     | HTML headings              | Websites                  |
| JSON           | JSON structure             | APIs, config files        |
| Code splitters | Functions/classes          | Source code               |

---

# Industry Usage

Here's what you'll typically see in production:

```text
PDF
        ↓
RecursiveCharacterTextSplitter

--------------------------------

Markdown Documentation
        ↓
MarkdownHeaderTextSplitter

--------------------------------

Website
        ↓
HTMLHeaderTextSplitter

--------------------------------

Python Codebase
        ↓
Language-aware Code Splitter

--------------------------------

JSON APIs
        ↓
RecursiveJsonSplitter
```

---

## 🎯 So what should **you** remember?

If someone wakes you up at 3 AM and asks:

> "Which text splitter should I use?"

Your answer should be:

* 📄 **PDF / Books / Articles** → `RecursiveCharacterTextSplitter` ⭐
* 📝 **Markdown Documentation** → `MarkdownHeaderTextSplitter`
* 🌐 **HTML Websites** → `HTMLHeaderTextSplitter`
* 📦 **JSON Data** → `RecursiveJsonSplitter`
* 💻 **Source Code** → Language-specific code splitters
* 🤖 **Need exact token limits** → `TokenTextSplitter`

This is exactly how experienced LangChain developers choose the right splitter for the job.
    