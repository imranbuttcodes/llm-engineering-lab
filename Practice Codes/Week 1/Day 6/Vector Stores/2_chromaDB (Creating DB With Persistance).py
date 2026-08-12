from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


embedding = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)


documents = [

    Document(
        page_content="Machine Learning is a subset of Artificial Intelligence.",
        metadata={"topic":"AI"}
    ),

    Document(
        page_content="Deep Learning uses Neural Networks.",
        metadata={"topic":"AI"}
    ),

    Document(
        page_content="Pizza originated in Italy.",
        metadata={"topic":"Food"}
    ),

    Document(
        page_content="Football is the world's most popular sport.",
        metadata={"topic":"Sports"}
    )

]


# It Will Create Database if not exist!
vector_store = Chroma(
    embedding_function = embedding,
    persist_directory='./chroma_db'
)

print("DataBase Created!")

vector_store.add_documents(documents)
query = "Tell me about AI"

result = vector_store.similarity_search(
    query,
    k=2)

print("Type:", type(result))
print('Type: ', type(result[0]))
print()
print(result)
print()

for doc in result:
    print(doc.page_content)
    print(doc.metadata)