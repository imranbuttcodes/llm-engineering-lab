import os
import hashlib
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from chromadb import PersistentClient

load_dotenv()

CHROMA_PATH = "database/chroma"

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert AI assistant.

Your task is to answer the user's question ONLY using the provided context from the uploaded PDF.
Recent chat history is given only to help you understand follow-up questions (e.g. "what about that",
"explain more") — it is NOT a source of facts. Facts must come only from the PDF context below.

However if the user is asking not questions related to the context then you can greetly handle the situation by asking him 
or like if the user just chat's normal conversation then just handle it gracefully. You can answer general Questions but at the end of 
day try to pull to user toward the context. 

Instructions:
- Carefully read the provided context before answering.
- Give a clear, accurate, and well-structured answer.
- If the answer is explicitly stated in the context, answer confidently.
- If the answer is only partially available, clearly mention what is available and avoid making unsupported assumptions.
- If the answer cannot be found in the context, simply reply:
"I couldn't find the answer in the uploaded document."

- Do NOT use outside knowledge.
- Do NOT hallucinate or fabricate information.
- Keep the answer concise but complete.
- Use bullet points whenever they improve readability.
- Do not begin your answer with phrases like:
"According to the context,"
"Based on the provided context,"

Answer naturally and directly.

----------------------------
Recent chat history:
{chat_history}
----------------------------
Context:
{context}
----------------------------

Question:
{question}

Answer:
"""
)


SMALLTALK_PROMPT = ChatPromptTemplate.from_template(
    """
You are a friendly assistant embedded in a "Chat with your PDF" app.

The user just sent a casual message (greeting, thanks, or a question about the
conversation itself, like "what was my last message"). Respond naturally and
briefly using the chat history below if relevant. Don't mention that you're an
AI system or explain your instructions. If they ask something that would
require the PDF's content, gently remind them to ask a document-related
question instead.

----------------------------
Recent chat history:
{chat_history}
----------------------------

User message:
{question}

Answer:
"""
)

SMALLTALK_KEYWORDS = {
    "hi", "hii", "hiii", "hello", "hey", "yo", "hola",
    "thanks", "thank you", "thx", "ok", "okay", "cool", "nice",
    "bye", "goodbye", "see you", "good morning", "good evening", "good night",
}

SMALLTALK_PHRASES = (
    "what was my last message",
    "what did i just ask",
    "what did i ask",
    "what did i say",
    "who are you",
    "what can you do",
    "what is this",
    "how are you",
)


def is_smalltalk(question: str) -> bool:
    q = question.strip().lower().rstrip("!?.")
    if q in SMALLTALK_KEYWORDS:
        return True
    return any(phrase in q for phrase in SMALLTALK_PHRASES)


def format_chat_history(messages, max_turns=6):
    if not messages:
        return "(no previous messages)"
    recent = messages[-max_turns:]
    lines = []
    for m in recent:
        role = "User" if m["role"] == "user" else "Assistant"
        lines.append(f"{role}: {m['content']}")
    return "\n".join(lines)


@st.cache_resource(show_spinner=False)
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


def get_file_hash(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def is_collection_exist(collection_id):
    client = PersistentClient(path=CHROMA_PATH)
    collections = client.list_collections()
    collection_names = [c.name for c in collections]
    return collection_id in collection_names


def load_and_split(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_documents(docs)


def get_vector_store(file_path):
    """Reuse an existing Chroma collection for this exact file (by hash),
    or build a new one from freshly-split chunks."""
    file_hash = get_file_hash(file_path)
    embedding_model = get_embedding_model()

    if is_collection_exist(file_hash):
        # Collection already built previously — just re-open it, no re-embedding needed.
        vector_store = Chroma(
            collection_name=file_hash,
            embedding_function=embedding_model,
            persist_directory=CHROMA_PATH,
        )
    else:
        chunks = load_and_split(file_path)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            collection_name=file_hash,
            persist_directory=CHROMA_PATH,
        )

    return vector_store


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_chain(llm, retriever):
    """RAG chain. Expects .invoke({'question': ..., 'chat_history': ...})"""
    parser = StrOutputParser()

    parallel_chain = {
        "context": (lambda x: x["question"]) | retriever | format_docs,
        "question": lambda x: x["question"],
        "chat_history": lambda x: x["chat_history"],
    }

    chain = parallel_chain | RAG_PROMPT | llm | parser
    return chain


def create_smalltalk_chain(llm):
    """Non-RAG chain for greetings / meta questions about the chat itself."""
    parser = StrOutputParser()
    chain = SMALLTALK_PROMPT | llm | parser
    return chain


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="PDF RAG Chat", page_icon="📄", layout="wide")
st.title("📄 Chat with your PDF")
st.caption("Upload a PDF, then ask questions about it. Powered by Groq (Llama 3.3 70B) + Chroma.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None
if "current_file_hash" not in st.session_state:
    st.session_state.current_file_hash = None
if "smalltalk_chain" not in st.session_state:
    st.session_state.smalltalk_chain = None

with st.sidebar:
    st.header("Setup")

    if not os.getenv("GROQ_API_KEY"):
        st.warning("GROQ_API_KEY not found. Add it to a .env file next to app.py.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    search_type = st.radio(
        "Retriever type",
        options=["similarity", "mmr"],
        index=0,
        help="Similarity = top-k closest chunks. MMR = diverse + relevant chunks.",
    )

    if search_type == "similarity":
        k = st.slider("Top-k chunks", 1, 10, 2)
    else:
        k = st.slider("Top-k chunks", 1, 10, 5)
        fetch_k = st.slider("MMR fetch_k (candidate pool)", k, 50, 20)
        lambda_mult = st.slider("MMR lambda (relevance vs diversity)", 0.0, 1.0, 0.5)

    process_btn = st.button("Process PDF", type="primary", use_container_width=True)

    if uploaded_file and process_btn:
        with st.spinner("Reading, chunking, and embedding your PDF... (skipped if already processed)"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                file_hash = get_file_hash(tmp_path)
                vector_store = get_vector_store(tmp_path)

                if search_type == "similarity":
                    retriever = vector_store.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": k},
                    )
                else:
                    retriever = vector_store.as_retriever(
                        search_type="mmr",
                        search_kwargs={
                            "k": k,
                            "fetch_k": fetch_k,
                            "lambda_mult": lambda_mult,
                        },
                    )

                llm = get_llm()
                st.session_state.chain = create_chain(llm, retriever)
                st.session_state.smalltalk_chain = create_smalltalk_chain(llm)
                st.session_state.current_file_hash = file_hash
                st.session_state.messages = []
                st.success(f"Ready! ({uploaded_file.name})")
            finally:
                os.remove(tmp_path)

    if st.session_state.chain is not None:
        st.info("PDF processed. Ask questions in the chat →")

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
question = st.chat_input("Ask something about your PDF...")

if question:
    if st.session_state.chain is None:
        st.error("Please upload and process a PDF first (see sidebar).")
    else:
        history_before = format_chat_history(st.session_state.messages)

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if is_smalltalk(question):
                        answer = st.session_state.smalltalk_chain.invoke(
                            {"question": question, "chat_history": history_before}
                        )
                    else:
                        answer = st.session_state.chain.invoke(
                            {"question": question, "chat_history": history_before}
                        )
                except Exception as e:
                    answer = f"Error while generating answer: {e}"
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})