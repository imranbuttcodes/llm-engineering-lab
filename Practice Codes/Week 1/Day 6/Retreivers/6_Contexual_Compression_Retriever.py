from dotenv import load_dotenv
import os

from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Sample Documents
# ============================================================

documents = [

    Document(
        page_content="""
Python was created by Guido van Rossum in 1991.

Python supports Object-Oriented Programming.

Python also supports Functional Programming.

Python is widely used in Artificial Intelligence,
Machine Learning, Data Science, Web Development,
Automation and Cybersecurity.

Python has one of the largest ecosystems of libraries.
""",
        metadata={"source": "python"}
    ),

    Document(
        page_content="""
Java was developed by James Gosling.

Java is platform-independent.

Java is heavily used for Android Development,
Enterprise Applications and Banking Systems.
""",
        metadata={"source": "java"}
    ),

    Document(
        page_content="""
Retrieval-Augmented Generation (RAG) combines
Large Language Models with external knowledge.

A retriever fetches relevant documents from
a Vector Database before the prompt is sent
to the LLM.

This improves factual accuracy and reduces hallucinations.
""",
        metadata={"source": "rag"}
    ),

    Document(
        page_content="""
Chroma is an open-source vector database.

It stores embeddings and performs semantic search
using vector similarity.

Chroma integrates seamlessly with LangChain.
""",
        metadata={"source": "chroma"}
    )

]

# ============================================================
# Embedding Model
# ============================================================

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ============================================================
# Vector Store
# ============================================================

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding
)

# ============================================================
# Base Retriever
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ============================================================
# Create Compressor
# ============================================================

compressor = LLMChainExtractor.from_llm(llm)

# ============================================================
# Contextual Compression Retriever
# ============================================================

compression_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=compressor
)

# ============================================================
# Query
# ============================================================

query = "Who created Python?"

# ============================================================
# Retrieve Compressed Documents
# ============================================================

docs = compression_retriever.invoke(query)

# ============================================================
# Display Results
# ============================================================

print("=" * 80)
print("Query:")
print(query)

print("\nRetrieved Documents:")
print("=" * 80)

for i, doc in enumerate(docs, start=1):

    print(f"\nDocument {i}")
    print("-" * 60)

    print("Source:")
    print(doc.metadata["source"])

    print("\nCompressed Content:")
    print(doc.page_content)