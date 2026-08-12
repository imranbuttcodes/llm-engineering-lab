from rank_bm25 import BM25Okapi


documents = [
    "LangGraph supports MemorySaver.",
    "FastAPI is used for backend APIs.",
    "BM25 is a keyword based retrieval algorithm.",
    "Vector databases use embeddings."
]



tokenized_docs = [doc.lower().split() for doc in documents]

print('tokenized_docs: ',tokenized_docs)

bm25 = BM25Okapi(tokenized_docs)

query = "What is FastAPI"


query_tokens = query.lower().split()

scores  = bm25.get_scores(query_tokens)

print(scores)
print()

retrieved_docs = bm25.get_top_n(
    query_tokens,
    documents,
    n=2
)

print(retrieved_docs)


