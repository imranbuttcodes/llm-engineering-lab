Perfect! 🔥 Now we're entering the **industry-standard text splitter**.

> If you remember **only one text splitter** in LangChain, make it this one.

Almost every RAG tutorial, production system, and enterprise application uses **`RecursiveCharacterTextSplitter`**.

---

# RecursiveCharacterTextSplitter

## First, why do we need another splitter?

Let's revisit `CharacterTextSplitter`.

Suppose we have this text:

```text
Machine Learning is a branch of Artificial Intelligence.

It enables computers to learn from data.

Principal Component Analysis (PCA) is a dimensionality reduction technique.

K-Means is a clustering algorithm.
```

Now suppose:

```python
chunk_size = 60
```

A normal `CharacterTextSplitter` may produce something like:

```text
Chunk 1
----------------
Machine Learning is a branch of Artificial Intelligence.
It en

Chunk 2
----------------
ables computers to learn from data.

Principal Component
```

😬

Problems:

* Split in the middle of **"enables"**
* Split in the middle of a sentence
* Context is damaged

---

# The Smarter Idea

Instead of cutting blindly...

Let's try to split **intelligently**.

Imagine asking:

> "Can I split at paragraphs first?"

If not...

> "Can I split at a newline?"

If not...

> "Can I split at a sentence?"

If not...

> "Can I split at a space?"

If not...

> "Okay... now I'll cut characters."

This is exactly what **RecursiveCharacterTextSplitter** does.

---

# Why is it called "Recursive"?

Because it **keeps trying different separators one after another** until the chunk fits.

Think of recursion here as:

```text
Paragraph

↓

Sentence

↓

Word

↓

Character
```

It recursively tries smaller and smaller separators.

---

# Visual Example

Suppose our document looks like:

```text
Paragraph 1

Paragraph 2

Paragraph 3
```

Chunk size:

```python
chunk_size = 100
```

First attempt:

```text
Can I split using:

"\n\n" ?

YES
```

Done!

---

Now suppose Paragraph 2 itself is huge.

```text
Paragraph 2
------------------------------------

Sentence 1

Sentence 2

Sentence 3

Sentence 4
```

Now it asks

```text
Can I split by paragraph?

NO
```

Next

```text
Can I split by newline?

YES
```

---

Suppose even one sentence is enormous.

It then tries

```text
Space
```

---

If even that fails...

Finally

```text
Character
```

---

# Default Separator Order

By default LangChain uses approximately:

```python
[
    "\n\n",   # Paragraph
    "\n",     # Line
    " ",      # Space
    ""        # Character
]
```

Notice

Characters are the **last resort**.

---

# Visualization

```text
Document

↓

Paragraph

↓

Sentence

↓

Words

↓

Characters
```

This preserves meaning much better.

---

# Constructor

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

Looks almost identical!

---

# Example 1

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Machine Learning is a field of AI.

It includes supervised learning.

It includes unsupervised learning.

Principal Component Analysis reduces dimensions.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-"*40)
```

---

Possible Output

```text
Chunk 1

Machine Learning is a field of AI.

It includes supervised learning.

----------------------------------------

Chunk 2

It includes supervised learning.

It includes unsupervised learning.

----------------------------------------

Chunk 3

Principal Component Analysis reduces dimensions.
```

Notice

✅ No broken words

✅ No broken sentences

Much cleaner.

---

# Splitting Documents

Exactly like before.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("book.pdf")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

print(len(chunks))
```

---

# Custom Separators

You can control the recursion order.

```python
splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ],
    chunk_size=300,
    chunk_overlap=50
)
```

Now it tries

```
Paragraph

↓

Newline

↓

Sentence

↓

Space

↓

Character
```

This often produces even better chunks because it prefers ending at sentence boundaries.

---

# Character vs Recursive

| Feature                                   | CharacterTextSplitter | RecursiveCharacterTextSplitter |
| ----------------------------------------- | --------------------- | ------------------------------ |
| Counts characters                         | ✅                     | ✅                              |
| Tries paragraph boundaries                | ❌                     | ✅                              |
| Tries sentence boundaries (if configured) | ❌                     | ✅                              |
| Tries spaces before cutting               | ❌                     | ✅                              |
| Breaks words frequently                   | ✅                     | Rarely                         |
| Better semantic chunks                    | ❌                     | ✅                              |
| Production use                            | Rare                  | ⭐⭐⭐⭐⭐                          |

---

# Industry Usage

Imagine building ChatGPT over:

* 📚 A 2,000-page medical textbook
* 📄 Legal contracts
* 📘 Research papers
* 📖 Documentation
* 💻 Source code

Almost everyone starts with:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

It's become a de facto standard because it balances simplicity, speed, and retrieval quality.

---

# Best Practices

There isn't a single "perfect" chunk size—it depends on your data—but common starting points are:

| Use Case       |                        Typical `chunk_size` | Typical `chunk_overlap` |
| -------------- | ------------------------------------------: | ----------------------: |
| Short articles |                                     300–500 |                      50 |
| PDFs & books   |                                    800–1200 |                 100–200 |
| Technical docs |                                    500–1000 |                     100 |
| Source code    | 100–300 lines (or language-aware splitters) |           Small overlap |

Treat these as starting values and tune them based on retrieval quality.

---

# Key Takeaway

Think of the two splitters like this:

* **CharacterTextSplitter** = ✂️ A simple ruler that cuts every *N* characters.
* **RecursiveCharacterTextSplitter** = 🧠 A careful editor that tries to preserve paragraphs, lines, and words before falling back to character-level cuts.

That's why **`RecursiveCharacterTextSplitter` is the default recommendation for most RAG applications**.

---

## Next Up 🚀

Once you're comfortable with this, we'll explore:

* **TokenTextSplitter** (splits by model tokens instead of characters)
* Why token-based splitting can be more accurate for LLM context limits
* When to choose token-based vs. recursive character-based splitting.
