from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Load and Split Documents
loader = PyPDFLoader('attention-is-all-you-need-Paper.pdf')
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 2. Setup Embeddings Model
emb_model = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

# Helper function to format retrieved documents into a string
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 3. Setup Vector Database (Safe creation without duplicate stacking)
persist_directory = './chroma.db'

if not os.path.exists(persist_directory):
    print("Creating new vector database...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=emb_model,
        persist_directory=persist_directory
    )
else:
    print("Loading existing vector database...")
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=emb_model
    )

# 4. Setup Retriever
retriever = vector_store.as_retriever(
    search_type='mmr',
    search_kwargs={
        'k': 4,
        'fetch_k': 10
    }
)

# 5. Define Prompt Template
template = """You are an expert assistant answering questions based strictly on the provided context.

Context:
{context}

Question: 
{question}

Answer Guidelines:
1. Answer the question thoroughly and concisely using ONLY the context provided above.
2. If the context does not contain the answer, reply exactly with: "I am sorry, but the provided text does not contain enough information to answer your question."
3. Do not assume, extrapolate, or bring in outside knowledge.
4. However you can answer general questions
Helpful Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# 6. Build the LCEL Chain Structure (FIXED HERE)
parallel_chain = {
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
}

# 7. Setup LLM and Output Parser
llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    api_key=os.getenv('GROQ_API_KEY')
)

parser = StrOutputParser()

# Final Executable Pipeline
rag_chain = parallel_chain | prompt | llm | parser

# 8. Interactive QA Chat Loop (FIXED HERE)
while True:
    question = input("Ask Anything: ")
    if question.strip().lower() == 'break':
        print("Exiting chat loop.")
        break

    if not question.strip():
        continue

    # Pass the question string directly into the chain
    result = rag_chain.invoke(question)

    print("\nAnswer:")
    print(result)
    print("-" * 50)
