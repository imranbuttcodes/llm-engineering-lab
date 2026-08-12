from langchain_huggingface import HuggingFaceEmbeddings


# single query embedding
embedding_model = HuggingFaceEmbeddings(
    model = 'sentence-transformers/all-MiniLM-L6-v2',
)

# result = embedding_model.embed_query("I'm Imran butt")

# print(str(result))


# docs Embddings

docs = [
    "Pakistan is My Country",
    "I failed My Exam",
    "I'm Happy"
]

result = embedding_model.embed_documents(docs)
    
print(result)


# from sentence_transformers import SentenceTransformer

# # Load a lightweight, fast model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Generate embeddings
# embeddings = model.encode(["The quick brown fox jumps over the lazy dog", "Another example sentence"])

# print(str(embeddings))