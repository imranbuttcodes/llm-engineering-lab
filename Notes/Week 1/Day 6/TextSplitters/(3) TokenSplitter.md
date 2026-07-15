Awesome! 🔥 This is where things get really interesting.

You've learned:

* ✅ CharacterTextSplitter
* ✅ RecursiveCharacterTextSplitter (industry standard)

Now we're moving to **TokenTextSplitter**, which introduces an important idea:

> **LLMs don't actually read characters—they read tokens.**

This distinction is crucial.

---

# TokenTextSplitter

## First, why do we need it?

Let's revisit what we've been doing.

CharacterTextSplitter works like this:

```text
ABCDEFGHIJKLMN...
```

It counts:

```text
1 character
2 characters
3 characters
...
```

Suppose:

```python
chunk_size = 1000
```

It means

> Maximum **1000 characters**.

But...

## Here's the problem.

### Do LLMs understand characters?

No.

They understand **tokens**.

When you send this prompt:

```text
What is Machine Learning?
```

The model **never sees characters directly**.

Instead it sees tokens.

For example (illustrative):

```text
"What"
"is"
"Machine"
"Learning"
"?"
```

or perhaps

```text
"What"
" is"
" Machine"
" Learning"
"?"
```

The exact tokens depend on the tokenizer.

---

# What is a Token?

A token is the **smallest unit processed by the LLM tokenizer**.

It might be:

* a whole word
* part of a word
* punctuation
* spaces
* numbers

Example:

```text
Machine Learning is awesome.
```

might become

```text
Machine
Learning
is
awesome
.
```

Another word:

```text
unbelievable
```

could become

```text
un
believ
able
```

Different models tokenize differently.

---

# Character vs Token

Suppose we have

```text
Artificial Intelligence
```

Character count

```text
23 characters
```

Token count

```text
3 tokens
```

They're completely different measurements.

---

Another example

```text
😂😂😂😂😂
```

Characters

```text
5
```

Tokens?

Maybe

```text
10
```

depending on the tokenizer.

---

# Why does this matter?

Imagine GPT has a limit

```text
8000 tokens
```

You split using characters.

```python
chunk_size = 4000
```

You think

> Great!

But...

4000 characters could become

```text
1200 tokens
```

or

```text
2500 tokens
```

or

```text
6000 tokens
```

depending on the language and content.

So **character count is only a rough approximation**.

---

# TokenTextSplitter solves this.

Instead of asking

> How many characters?

It asks

> **How many tokens?**

---

# Visualization

Character splitter

```text
Document

↓

1000 Characters

↓

1000 Characters

↓

1000 Characters
```

---

Token splitter

```text
Document

↓

512 Tokens

↓

512 Tokens

↓

512 Tokens
```

Exactly what the LLM understands.

---

# Constructor

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
```

Looks almost identical!

The difference is

```python
chunk_size = 200
```

means

```text
200 TOKENS
```

NOT

```text
200 characters
```

---

# Example

```python
from langchain_text_splitters import TokenTextSplitter

text = """
Machine Learning is one of the most important fields of Artificial Intelligence.
It is widely used in healthcare, finance, robotics, and autonomous vehicles.
"""

splitter = TokenTextSplitter(
    chunk_size=20,
    chunk_overlap=5
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-"*40)
```

Notice

You specify

```python
20
```

meaning

```text
20 tokens
```

not characters.

---

# Splitting Documents

Exactly the same API.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

loader = PyPDFLoader("book.pdf")

docs = loader.load()

splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)
```

---

# Why Production Systems Like It

Suppose you're using

```text
GPT-4
```

Maximum context

```text
128K TOKENS
```

NOT

```text
128K CHARACTERS
```

So splitting by tokens guarantees you're respecting the model's actual limit.

---

# Character vs Token Example

Sentence

```text
Machine Learning is amazing.
```

Character count

```text
29
```

Token count (illustrative)

```text
Machine
Learning
is
amazing
.
```

Only

```text
5 tokens
```

Huge difference.

---

# Another Example

```text
Supercalifragilisticexpialidocious
```

Characters

```text
34
```

Tokens?

Maybe

```text
Super
cali
frag
ilistic
...
```

Many tokens.

Again,

Characters ≠ Tokens.

---

# Comparison

| Feature                 | Character | Recursive | Token   |
| ----------------------- | --------- | --------- | ------- |
| Splits by characters    | ✅         | ✅         | ❌       |
| Preserves paragraphs    | ❌         | ✅         | Depends |
| Uses tokenizer          | ❌         | ❌         | ✅       |
| Accurate for LLM limits | ❌         | ❌         | ✅       |
| Production ready        | ⭐⭐        | ⭐⭐⭐⭐⭐     | ⭐⭐⭐⭐    |

---

# Should you always use TokenTextSplitter?

Not necessarily.

### Use **RecursiveCharacterTextSplitter** when:

* 📚 PDFs
* 📖 Books
* 📰 Articles
* 📄 Documentation

It preserves readable chunks and is a fantastic default.

---

### Use **TokenTextSplitter** when:

* 🤖 You need precise control over the model's context window
* 💰 You're optimizing token usage and cost
* 📏 You must enforce strict token limits

---

# A subtle limitation

`TokenTextSplitter` is **token-aware**, but it **isn't inherently structure-aware**. It focuses on token counts, not preserving paragraphs or sentences. That means it can still split in the middle of an idea if that's where the token boundary falls.

For many RAG applications, developers therefore prefer **RecursiveCharacterTextSplitter**, which creates more natural chunks, even though the chunk size is measured approximately by characters.

---

# Industry Perspective

A common workflow is:

```text
Large PDF
      │
      ▼
RecursiveCharacterTextSplitter
      │
      ▼
Natural, readable chunks
      │
      ▼
Embeddings
      │
      ▼
Vector Database
```

If an application has **very strict token budgets** (for example, sending chunks directly to an LLM with a hard token limit), teams may instead choose a token-based splitter or combine recursive splitting with token-aware sizing.

---

## Up Next 🚀

We've now covered the three core splitters:

* ✅ CharacterTextSplitter
* ✅ RecursiveCharacterTextSplitter
* ✅ TokenTextSplitter

The next interesting category is **structure-aware splitters**, such as **MarkdownHeaderTextSplitter**, **HTMLHeaderTextSplitter**, and **Recursive JSON splitters**, which preserve the hierarchy of documents instead of just their size. These are especially useful when working with documentation websites, Markdown files, and structured data.
