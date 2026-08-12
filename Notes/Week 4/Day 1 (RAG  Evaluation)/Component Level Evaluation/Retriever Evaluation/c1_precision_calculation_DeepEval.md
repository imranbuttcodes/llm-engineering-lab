Yes bro. This one is **really important**, because DeepEval's **Contextual Precision is not ordinary `Precision@K`**.

DeepEval uses an **LLM-as-a-judge + ranking-aware precision calculation**. ([DeepEval][1])

## 1. What is DeepEval trying to measure?

It asks:

> **Are the relevant retrieved chunks ranked higher than the irrelevant ones?**

So:

```text
Query
  ↓
Retriever
  ↓
Ranked retrieval_context
  ↓
LLM Judge labels each chunk
  ↓
Relevant / Not Relevant
  ↓
Weighted cumulative precision
```

This is why DeepEval says Contextual Precision is particularly useful for evaluating the **ranking/reranking** part of a retriever. ([DeepEval][1])

---

# 2. Example

Suppose our query is:

> "What is the tuition refund deadline?"

Retriever returns:

```text
Rank 1 → DOC-A  ❌ irrelevant
Rank 2 → DOC-B  ✅ relevant
Rank 3 → DOC-C  ❌ irrelevant
Rank 4 → DOC-D  ✅ relevant
Rank 5 → DOC-E  ❌ irrelevant
```

The LLM judge first determines relevance of each retrieved node **using the input and expected output**. ([DeepEval][1])

So conceptually:

```text
r₁ = 0
r₂ = 1
r₃ = 0
r₄ = 1
r₅ = 0
```

Then DeepEval calculates a **weighted cumulative precision**:

[
CP = \frac{1}{R}\sum_{k=1}^{n}
\left(
\frac{\text{relevant nodes up to }k}{k}
\times r_k
\right)
]

where `R` is the total number of relevant nodes. ([DeepEval][1])

---

# 3. Let's calculate it

Our ranking:

```text
Rank   Relevant?   Precision up to rank
1      ❌           0/1 = 0
2      ✅           1/2 = 0.50
3      ❌           1/3 = 0.33
4      ✅           2/4 = 0.50
5      ❌           2/5 = 0.40
```

Only relevant positions contribute because `r_k = 1`.

So:

```text
CP = (0.50 + 0.50) / 2
   = 0.50
```

Therefore:

**Contextual Precision = 0.50**

The important thing is that the relevant chunks were **buried at ranks 2 and 4**.

---

# 4. Now look at why ranking matters

Imagine the exact same relevant chunks, but the retriever returns:

```text
Rank 1 → DOC-B  ✅
Rank 2 → DOC-D  ✅
Rank 3 → DOC-A  ❌
Rank 4 → DOC-C  ❌
Rank 5 → DOC-E  ❌
```

Now:

```text
Rank 1 → 1/1 = 1.00
Rank 2 → 2/2 = 1.00
```

So:

```text
CP = (1.00 + 1.00) / 2
   = 1.00
```

🔥 **Same relevant documents. Completely different Contextual Precision.**

That's the key.

---

# 5. So Precision vs Recall

This gives us a beautiful distinction:

### Contextual Recall

> **Did we retrieve enough information to answer the question?**

```text
Ideal Answer
     ↓
Claims
     ↓
Retrieved Context
     ↓
How many claims are supported?
```

DeepEval calculates it as:

[
\text{Contextual Recall}
========================

\frac{\text{Attributable Statements}}
{\text{Total Statements}}
]

([DeepEval][2])

---

### Contextual Precision

> **Did we put the relevant information high in the ranking?**

```text
Retrieved Context

1. ❌
2. ✅
3. ❌
4. ✅
5. ❌

        ↓

Ranking-aware precision
```

DeepEval's formula is the weighted cumulative precision described above. ([DeepEval][1])

---

# 6. And Contextual Relevancy is different again

DeepEval also has **Contextual Relevancy**.

It asks:

> **How much of the retrieved context is actually relevant to the question?**

It extracts statements from the retrieved context and judges whether those statements are relevant to the input. ([DeepEval][3])

So our retriever evaluation becomes:

| Metric                   | Question                                                     |
| ------------------------ | ------------------------------------------------------------ |
| **Contextual Recall**    | Did we retrieve the information needed?                      |
| **Contextual Precision** | Did we rank useful information above irrelevant information? |
| **Contextual Relevancy** | How much of what we retrieved is actually relevant?          |

DeepEval itself categorizes these three as its main **retriever metrics** for RAG. ([DeepEval][4])

### The mental model I want you to remember

```text
                 RETRIEVER
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
      RECALL     PRECISION    RELEVANCY
        │           │            │
        ▼           ▼            ▼
   "Did we get    "Did we      "Is the
    enough?"       rank it?"     stuff useful?"
```

And **this is why you shouldn't think of DeepEval Contextual Precision as simply `relevant chunks / retrieved chunks`**.

It is **ranking-aware** and uses an LLM judge to determine which retrieved nodes are relevant before applying the weighted precision calculation. ([DeepEval][1])

[1]: https://deepeval.com/docs/metrics-contextual-precision?utm_source=chatgpt.com "Contextual Precision | DeepEval - The LLM Evaluation Framework"
[2]: https://deepeval.com/docs/metrics-contextual-recall?utm_source=chatgpt.com "Contextual Recall | DeepEval - The LLM Evaluation Framework"
[3]: https://deepeval.com/docs/metrics-contextual-relevancy?utm_source=chatgpt.com "Contextual Relevancy | DeepEval - The LLM Evaluation Framework"
[4]: https://deepeval.com/docs/metrics-introduction?utm_source=chatgpt.com "Introduction to LLM Evaluation Metrics | DeepEval - The LLM Evaluation Framework"
