from dotenv import load_dotenv
import os

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.retrievers import MultiQueryRetriever


# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

# =====================================================
# Create Sample Documents
# =====================================================

documents = [
    Document(
        page_content="""
        Retrieval-Augmented Generation (RAG) is a technique that combines
        Large Language Models with external knowledge retrieved from a
        vector database before generating a response.
        """,
        metadata={"source": "rag_intro"}
    ),

    Document(
        page_content="""
        Vector Databases such as Chroma, FAISS, Pinecone and Weaviate
        store vector embeddings and perform semantic similarity search.
        """,
        metadata={"source": "vector_db"}
    ),

    Document(
        page_content="""
        Embeddings are numerical vector representations of text.
        Similar texts produce vectors that are close together in
        vector space.
        """,
        metadata={"source": "embeddings"}
    ),

    Document(
        page_content="""
        Retrieval systems fetch relevant information from a knowledge base
        before passing it to the language model.
        """,
        metadata={"source": "retrieval"}
    ),

    Document(
        page_content="""
        Context injection improves the factual accuracy of Large Language
        Models by supplying relevant documents inside the prompt.
        """,
        metadata={"source": "context"}
    ),

    Document(
        page_content="""
        External knowledge allows LLMs to answer questions using
        information that was not present during training.
        """,
        metadata={"source": "external_knowledge"}
    )
]

# =====================================================
# Embedding Model
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# Create Chroma Vector Store
# =====================================================

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model
)

# =====================================================
# Convert into Retriever
# =====================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# =====================================================
# Initialize LLM
# =====================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# Create MultiQueryRetriever
# =====================================================

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

# =====================================================
# Query
# =====================================================

query = "How does RAG work?"

# =====================================================
# Retrieve Documents
# =====================================================
import logging

logging.basicConfig(level=logging.INFO)

logging.getLogger(
    "langchain_classic.retrievers.multi_query"
).setLevel(logging.INFO)

results = multi_query_retriever.invoke(query)

# =====================================================
# Display Results
# =====================================================

print("=" * 80)
print("Original Query:")
print(query)

print("\n" + "=" * 80)
print(f"Retrieved {len(results)} Documents")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nDocument {i}")
    print("-" * 60)

    print("Source :", doc.metadata["source"])
    print("Content:")
    print(doc.page_content.strip())