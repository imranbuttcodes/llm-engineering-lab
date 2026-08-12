YES bro — **you've spotted a very important problem in retrieval evaluation.** This is exactly the kind of thing that matters when building a serious evaluation framework.

And I've saved this for the future mind map.

## The key distinction: `Top-K` vs `chunking`

These two changes behave very differently.

### Case 1 — Change `Top-K`

Suppose your current chunks are:

```
DOC-01
 ├── CHUNK-01
 ├── CHUNK-02
 ├── CHUNK-03
 └── CHUNK-04

```

You evaluate:

```
Top-K = 3

```

and get:

```
Recall@3 = 0.65

```

Then you change:

```
Top-K = 5

```

**Nothing about the chunks changes.**

You're simply asking:

> "Instead of looking at the first 3 retrieved chunks, what happens if I look at the first 5?"

So the same golden labels remain valid.

```
Same chunks
    ↓
Top-3 → evaluate
Top-5 → evaluate
Top-10 → evaluate

```

This is perfectly fine.

---

# Case 2 — Change chunking

Now suppose you have:

```
chunk_size = 500
overlap = 50

```

and your corpus becomes:

```
DOC-01
 ├── CHUNK-A
 ├── CHUNK-B
 ├── CHUNK-C

```

Your golden dataset might say:

```
{
  "question": "What is the refund deadline?",
  "relevant_chunks": ["CHUNK-B"]
}

```

Now you change:

```
chunk_size = 300
overlap = 50

```

You might get:

```
DOC-01
 ├── CHUNK-X
 ├── CHUNK-Y
 ├── CHUNK-Z
 ├── CHUNK-W

```

**CHUNK-B doesn't even exist anymore.**

So yes:

> 🔥 **A chunk-level golden dataset can become invalid when you change the chunking strategy.**

That's a real evaluation-design issue.

---

# The solution: separate Document IDs from Chunk IDs

This is extremely important.

Instead of thinking:

```
DOC-01 → CHUNK-42

```

as your only ground truth, maintain:

```
SOURCE DOCUMENT
       │
       ▼
   DOC-01
       │
   ┌───┼────┐
   ▼   ▼    ▼
 C-01 C-02 C-03

```

Your **stable ground truth** should preferably identify the **source document / relevant passage**, rather than being permanently tied to an arbitrary chunk ID.

For example:

```
{
  "question": "What is the refund deadline?",
  "relevant_documents": ["DOC-03"]
}

```

Then regardless of chunking:

### Version A

```
DOC-03
 ├── C1
 ├── C2 ← contains answer
 └── C3

```

### Version B

```
DOC-03
 ├── C1
 ├── C2
 ├── C3 ← contains answer
 ├── C4
 └── C5

```

The **gold source remains DOC-03**.

You can then determine whether the retrieved chunks came from the correct source.

---

# But there's an even better approach

For serious RAG evaluation, you can maintain **two levels of ground truth**:

```
Golden Dataset
       │
       ├── Stable source-level labels
       │
       │     DOC-03
       │
       └── Versioned chunk-level labels
             
             Chunking v1
             └── C-42

             Chunking v2
             └── C-87

```

Then:

### Stable evaluation

Useful for comparing:

```
Embedding A
vs
Embedding B
vs
Retriever A
vs
Retriever B

```

without changing the corpus structure.

### Version-specific evaluation

Useful when you're specifically testing:

```
chunk_size 500
      vs
chunk_size 300
      vs
semantic chunking

```

because the chunks themselves have changed.

---

# This gives us an important evaluation rule

### `Top-K` experiment

```
Chunking unchanged
Gold unchanged

K=1
K=3
K=5
K=10

```

✅ Directly comparable.

---

### Chunking experiment

```
Chunking changes
       ↓
Chunks change
       ↓
Chunk IDs change
       ↓
Chunk-level gold labels may become invalid

```

⚠️ You need **stable source-level ground truth** or a **new/versioned chunk-level annotation**.

---

# And this is actually why our golden JSON should be designed carefully

Instead of only:

```
{
  "question": "What is the refund deadline?",
  "relevant_chunk_ids": ["chunk_42"]
}

```

I'd prefer our base evaluation dataset to contain:

```
{
  "question": "What is the refund deadline?",
  "relevant_doc_ids": ["DOC-03"]
}

```

Then our retrieval experiment can record:

```
Retrieved:
CHUNK-17 → DOC-03
CHUNK-22 → DOC-07
CHUNK-31 → DOC-04

```

and evaluate against:

```
Gold:
DOC-03

```

That makes our evaluation much more robust to chunking experiments.

---

## 🔥 The bigger lesson

You just discovered something beyond "what is Recall?"

It's:

> **Evaluation datasets themselves have assumptions and dependencies.**

Your evaluation result of `0.65` is only meaningful if we know **what exactly is being held constant**.

So when we run experiments, we should track:

```
Experiment
│
├── Corpus version
├── Document version
├── Chunking strategy
│   ├── chunk size
│   └── overlap
├── Embedding model
├── Retriever
├── Top-K
├── Reranker
└── Evaluation dataset version

```

Then we can actually say:

> **Experiment B improved Recall\@5 from 0.65 → 0.82 while keeping the corpus and evaluation protocol constant.**

That's a legitimate evaluation result.

Not:

> "I changed five things and recall went up, yay." 😄

This **gold-label stability + chunking-versioning issue** is absolutely something we'll put into your eventual **RAG Evaluation mind map**.
