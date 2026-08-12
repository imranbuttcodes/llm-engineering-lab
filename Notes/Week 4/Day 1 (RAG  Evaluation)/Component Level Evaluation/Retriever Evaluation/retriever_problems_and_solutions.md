Absolutely bro. Let's make this **clean and exam/interview-ready**.

# Retriever Failures → Solutions

| #      | Retriever issue                            | What happens                                                                   | Typical solution                                                      |
| ------ | ------------------------------------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **1**  | **Irrelevant retrieval**                   | Retrieves documents unrelated to the query                                     | Better embeddings, hybrid search, reranking, improve chunking         |
| **2**  | **Missing relevant documents**             | Important information exists but isn't retrieved                               | Better embeddings, hybrid retrieval, query expansion, increase `K`    |
| **3**  | **Poor ranking**                           | Relevant document is retrieved but ranked too low                              | **Reranker**, improve retrieval scoring, tune `K`                     |
| **4**  | **Lexical mismatch**                       | Query and document use different words for the same concept                    | Dense embeddings / hybrid BM25 + vector search                        |
| **5**  | **Semantic mismatch**                      | Retriever thinks two concepts are similar when they aren't                     | Better embedding model, reranker, domain-specific embeddings          |
| **6**  | **Ambiguous query**                        | Query doesn't provide enough information                                       | Query rewriting, clarification question, query expansion              |
| **7**  | **Bad chunking**                           | Relevant information is split or context is incomplete                         | Tune chunk size, overlap, semantic/recursive chunking                 |
| **8**  | **Wrong `Top-K`**                          | Too few results → missing information; too many → noisy context                | Tune `K`, evaluate Recall@K and Precision@K                           |
| **9**  | **Redundant results**                      | Multiple retrieved chunks contain almost the same information                  | MMR, deduplication, diversity-aware reranking                         |
| **10** | **Topic-relevant but answer-insufficient** | Retrieved chunks discuss the right topic but don't contain the specific answer | Better chunking, query rewriting, reranking, multi-query retrieval    |
| **11** | **Long/noisy context**                     | Relevant chunk is buried among irrelevant chunks                               | Reranking, filtering, smaller `K`, context compression                |
| **12** | **Query complexity**                       | One query contains multiple information needs                                  | Query decomposition / multi-query retrieval                           |
| **13** | **Domain-specific terminology**            | General embeddings don't understand specialized vocabulary                     | Domain-specific embeddings, hybrid search, fine-tuning when justified |
| **14** | **Outdated/incorrect knowledge**           | Retriever returns stale or invalid documents                                   | Metadata filtering, document versioning, freshness filters            |
| **15** | **Metadata ignored**                       | Correct content exists but wrong source/date/category is retrieved             | Metadata filtering + hybrid retrieval                                 |

---

## The important ones to memorize first

Don't try to memorize all 15 immediately.

The **core retriever failure taxonomy** is:

```text
                 RETRIEVER FAILURES
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
    WRONG DOC        WRONG RANK       MISSING DOC
       │                │                │
   Precision          MRR/NDCG         Recall
       │
       └─────────────────────────────────┐
                                         ▼
                              RETRIEVAL QUALITY
                                         │
                  ┌──────────────────────┼──────────────────┐
                  ▼                      ▼                  ▼
               Chunking                Query             Redundancy
               problems               problems            problems
                  │                      │                  │
                  ▼                      ▼                  ▼
             Re-chunking          Rewrite/decompose     MMR/dedup
```

### And remember this distinction:

**Wrong documents → Precision problem**

**Missing documents → Recall problem**

**Correct document too low → Ranking problem**

**Correct topic but insufficient information → Chunking/query/ranking problem**

---

# How we diagnose them

This is where **evaluation metrics connect to failure analysis**:

```text
Retriever
   │
   ▼
Top-K results
   │
   ├── Precision@K ──► Are results relevant?
   │
   ├── Recall@K ────► Did we find what we needed?
   │
   ├── Hit Rate@K ──► Did we find at least one relevant result?
   │
   ├── MRR ─────────► How high was the first relevant result?
   │
   └── NDCG ────────► Is the whole ranking good?
```

Then, if the metrics show a problem, **we investigate the failure category and apply the appropriate fix**.

That's the mindset you want:

> **Don't blindly optimize the retriever. First identify how it fails → choose the metric that exposes that failure → apply the appropriate fix → rerun the evaluation suite.**
