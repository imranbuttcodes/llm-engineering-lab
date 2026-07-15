from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

results = vector_store.similarity_search("Tell me about AI", k = 2)

print("Without Similarity Scores")
print()

for doc in results:
    print(doc.page_content)
    

    
results = vector_store.similarity_search_with_score(
    "Tell me about AI",
    k=4
)


print("With Similarity Scores")
print()

for doc, score in results:
    print(score)
    print(doc.page_content)
    print("-" * 50)


