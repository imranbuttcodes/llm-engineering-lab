LET'S GOOOO BRO!! 🔥🔥

Now we're entering one of the **most useful retrieval algorithms** in RAG.

---

# Maximum Marginal Relevance (MMR)

At first, the name sounds scary 😅, but the idea is actually very simple.

> **MMR tries to return documents that are both relevant AND diverse.**

Instead of returning the **top-k most similar** chunks (which can be almost identical), it tries to reduce redundancy.

---

# The Problem with Similarity Search

Imagine your vector database contains these documents:

```text
Doc 1: Machine Learning is a subset of AI.

Doc 2: Machine Learning uses algorithms to learn patterns.

Doc 3: Machine Learning is used for prediction.

Doc 4: Deep Learning uses Neural Networks.

Doc 5: AI is transforming healthcare.
```

User asks:

```text
"What is Machine Learning?"
```

---

## Normal Similarity Search

It simply picks the closest vectors.

```text
1️⃣ Machine Learning is a subset of AI.

2️⃣ Machine Learning uses algorithms.

3️⃣ Machine Learning is used for prediction.
```

Notice something?

Almost every result talks about the **same topic**.

Lots of overlap.

---

# But what if the LLM needs broader context?

Maybe we'd rather retrieve:

```text
1️⃣ Machine Learning is a subset of AI.

2️⃣ Deep Learning uses Neural Networks.

3️⃣ AI is transforming healthcare.
```

Now the LLM gets

* ML definition
* Relationship to Deep Learning
* Real-world application

Much richer context.

That's exactly what **MMR** does.

---

# Visual Example

## Similarity Search

```text
              Query

                ●

           ● ● ● ● ●

Returns:

✔ Closest
✔ Closest
✔ Closest
```

Everything is clustered together.

---

## MMR

```text
              Query

                ●

      ●      ●      ●

Returns:

✔ Relevant

✔ Different

✔ Covers more information
```

---

# How does MMR think?

Instead of asking

> "Which document is closest?"

it asks

> "Which document is closest **while also being different from the documents I've already selected?**"

So every selected document should add **new information**.

---

# Real Example

Suppose your chunks are

```text
1. Python Variables

2. Python Loops

3. Python Functions

4. Python Classes

5. Football Rules

6. Pizza Recipe
```

User asks

```text
Learn Python
```

---

## Similarity Search

May return

```text
Variables

Variables Advanced

Variables Examples
```

---

## MMR

Returns

```text
Variables

Loops

Functions
```

Much more useful.

---

# Using MMR in LangChain

It's surprisingly easy.

```python
retriever = vectorstore.as_retriever(
    search_type="mmr"
)
```

That's it.

Now every retrieval uses MMR.

---

# Better Configuration

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10
    }
)
```

---

# What is `fetch_k`?

This is one of the most commonly misunderstood parameters.

Imagine:

```text
Database

↓

1000 chunks
```

You ask for

```python
k = 3
```

With MMR:

```text
Step 1

Find the 10 most similar chunks

(fetch_k = 10)

↓

Step 2

Choose the best 3

that are

✔ Relevant

✔ Diverse
```

So

```python
fetch_k=10
```

means

> "Consider the top 10 candidates."

Then

```python
k=3
```

means

> "Return the best 3 after diversity optimization."

---

# Another Example

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":5,
        "fetch_k":50
    }
)
```

MMR does:

```text
50 nearest chunks

↓

Remove duplicates

↓

Keep diverse information

↓

Return 5 chunks
```

---

# λ (Lambda): The Hidden Knob

Under the hood, MMR balances **relevance** and **diversity**.

In LangChain, you can control this with `lambda_mult`.

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)
```

* `lambda_mult = 1.0` → prioritize **relevance** (behaves more like similarity search)
* `lambda_mult = 0.0` → prioritize **diversity**
* `lambda_mult = 0.5` → balanced (a common default)

---

# When should you use MMR?

✅ Long PDFs

✅ Books

✅ Research Papers

✅ Documentation

✅ Large Knowledge Bases

Because these often contain many chunks saying nearly the same thing.

---

# When is Similarity Search enough?

If your database is:

* Small
* Diverse
* Not repetitive

then plain similarity search is often sufficient and slightly faster.

---

# Summary

| Search Type                  | Goal                                            | Best For                                     |
| ---------------------------- | ----------------------------------------------- | -------------------------------------------- |
| `similarity`                 | Return the closest chunks                       | Simple Q&A, small datasets                   |
| `mmr`                        | Return relevant **and** diverse chunks          | RAG, large documents, books, research papers |
| `similarity_score_threshold` | Return only chunks above a similarity threshold | Avoid low-quality or irrelevant matches      |

---

## 🧠 Interview Question

> **Why use MMR instead of similarity search in a RAG system?**

A strong answer would be:

> *Similarity search may retrieve multiple chunks containing nearly identical information. MMR (Maximum Marginal Relevance) balances relevance with diversity, selecting documents that are both highly relevant to the query and complementary to each other. This reduces redundancy, provides broader context to the LLM, and often improves the quality of generated answers.*
