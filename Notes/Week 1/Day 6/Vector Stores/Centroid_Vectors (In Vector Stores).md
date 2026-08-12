In the context of **vector stores** (used in AI, semantic search, and RAG systems), a **centroid vector** is the **average embedding vector of a group of vectors**.

Think of it as the **"center of meaning"** for a collection of documents.

### Intuition

Imagine you have embeddings for five documents about **cats**:

```
Doc 1 → [0.2, 0.8, 0.5, ...]
Doc 2 → [0.3, 0.7, 0.6, ...]
Doc 3 → [0.1, 0.9, 0.4, ...]
Doc 4 → [0.2, 0.8, 0.6, ...]
Doc 5 → [0.3, 0.7, 0.5, ...]
```

Instead of storing just these five separately, you can compute their **centroid**:

```
Centroid = (Doc1 + Doc2 + Doc3 + Doc4 + Doc5) / 5
```

This new vector sits near the "middle" of all five vectors in the embedding space.

---

### Why use centroid vectors?

They have several applications.

#### 1. Representing a Cluster

Suppose you clustered 10,000 documents into topics.

```
Cluster A (Cats)
    ↓
Doc1
Doc2
Doc3
Doc4

        ↓

Centroid A
```

Instead of saying:

> "This cluster consists of thousands of vectors."

You can summarize it with **one centroid vector** that represents the average semantic meaning.

---

#### 2. Faster Search

Imagine you have 100 clusters.

When a query comes in:

```
Query
   ↓
Compare with 100 centroids
   ↓
Choose the closest cluster
   ↓
Search only inside that cluster
```

Instead of comparing against **1 million vectors**, you first compare against **100 centroid vectors**, which is much faster.

This is how many Approximate Nearest Neighbor (ANN) indexes speed up search.

---

#### 3. Topic Representation

A centroid can represent an entire topic.

For example:

```
Documents:

• Cats are pets
• Kittens drink milk
• Felines hunt mice
• Domestic cats are playful

↓

Centroid Vector

≈ "Average meaning of cats"
```

You can compare a new query to this centroid to determine whether it's about cats.

---

### Geometric intuition

Imagine vectors as points in space.

```
            Doc2

      Doc1      Doc3

          ●
      Centroid

   Doc4        Doc5
```

The centroid lies near the middle of the group.

---

### How is it computed?

For vectors

```
v1
v2
...
vn
```

the centroid is

```
centroid = (v1 + v2 + ... + vn) / n
```

That is, you average each dimension independently.

For example:

```
v1 = [2, 4]
v2 = [4, 6]
v3 = [6, 8]

Centroid:

[(2+4+6)/3,
 (4+6+8)/3]

=

[4, 6]
```

---

### Do vector databases store centroids?

It depends on the implementation.

Some vector databases and ANN algorithms (such as IVF indexes in FAISS) **do** maintain centroid vectors internally to organize vectors into clusters for efficient search.

Others simply store individual embeddings and do **not** compute centroids unless you explicitly create them.

---

### Summary

A **centroid vector** is the **average embedding of a group of vectors**. It acts as the semantic "center" of that group and is commonly used for:

* **Representing a cluster** of similar documents.
* **Speeding up similarity search** by narrowing the search to relevant clusters.
* **Summarizing a topic** with a single representative vector.
* **Organizing embeddings** in ANN indexes such as IVF.

In short, if each embedding represents one document, a **centroid vector represents the average meaning of many related documents**.
