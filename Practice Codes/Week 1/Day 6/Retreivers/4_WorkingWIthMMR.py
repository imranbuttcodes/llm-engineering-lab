from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


docs = [
    Document(page_content="LangChain makes it easy to work with LLMs."),
    Document(page_content="LangChain is used to build LLM based applications."),
    Document(page_content="Chroma is used to store and search document embeddings."),
    Document(page_content="Embeddings are vector representations of text."),
    Document(page_content="MMR helps you get diverse results when doing similarity search."),
    Document(page_content="LangChain supports Chroma, FAISS, Pinecone, and more."),
]

embedding = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)


vector_store = Chroma.from_documents(
    embedding= embedding,
    documents=docs    
)

query = ''

retriever = vector_store.as_retriever(
    search_type = 'mmr',
    search_kwargs = {'k': 2, 'fetch_k':  3, 'lambda_mult': 0.5} # lambda ranges from 0 - 1 and the more the lower value is more the diverse resutls we get
)

docs = retriever.invoke(
    'What is langchain?'
)

print(type(docs))
print(docs)

for doc in docs:
    print(doc.page_content)
    print()