# %%
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
import nltk

# %%
load_dotenv()

# %%
# docs = [
#     PyPDFLoader('documents/book1.pdf').load() + 
#     PyPDFLoader('documents/book2.pdf').load() + 
#     PyPDFLoader('documents/book3.pdf').load()  
# ]


# %%
# docs = docs[0]

# %%
# print("Total Docs: ", len(docs))

# for d in docs[:3]:
#     print(d.page_content)

# %%
# chunks = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 150).split_documents(docs)


# %%
# print(len(chunks))
# print()
# for c in chunks[:3]:
#     print(c.page_content)
#     print()

# %%
embedding_model = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

# %%
# # 3) Clean text to avoid UnicodeEncodeError (surrogates from PDF extraction)
# for d in chunks:
#     d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

# %%
# vector_store = Chroma.from_documents(
#     embedding=embedding_model,
#     documents=chunks,
#     persist_directory='c-rag-db/chroma-crag.db'
# )

# %% [markdown]
# ## Load Existing Docs

# %%
vector_store = Chroma(
    embedding_function=embedding_model,
    persist_directory='c-rag-db/chroma-crag.db'
)

# %%
retriever = vector_store.as_retriever(search_type = 'similarity' , kwargs={
    'search_kwargs': {
        'k': 4
    }
})

# %%
LOWER_THRESHOLD = 0.3
UPPER_THRESHOLD = 0.7

# %%
class State(BaseModel):
    question: str

    docs: List[Document] = Field(default_factory=list)
    good_docs: List[Document] = Field(default_factory=list)
    web_docs: List[Document] = Field(default_factory=list)
    strips: List[str] = Field(default_factory=list)
    kept_strips: List[str] = Field(default_factory=list)

    refine_context: str = ""
    web_query: str = ""
    VERDICT: str = ""
    reason: str = ""
    answer: str = ""

# %%
gpt_llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# groq_llm = ChatGroq(
#     model = 'llama-3.3-70b-versatile',
#     api_key=os.getenv('GROQ_API_KEY')
# )

groq_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# %%
class DocScoreSchema(BaseModel):
    score: float = Field(
        description="Score reflecting document relevance, between 0.0 and 1.0",
        ge=0.0,  # Greater than or equal to 0.0
        le=1.0   # Less than or equal to 1.0
    )

# %%
eval_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ('system', 'You are a strict retrieval evaluator for RAG. You will be given one retrieved '
                   'chunk (as in one document) and a question. Return a relevance score between zero '
                   'and one. One means the chunk alone is sufficient to answer fully, and zero means '
                   'the chunk is irrelevant. Be conservative with high scores.'),
        ('human', 'Question: {question}\n\nChunk: {chunk}')
    ]
)

llm_evaluate_chain = eval_prompt | groq_llm.with_structured_output(DocScoreSchema)

# %%
# -----------------------------
# Retrieve
# -----------------------------
def retrieve_node(state: State):
    q = state.question
    return {"docs": retriever.invoke(q)}


# %%
def eval_each_doc_node(state: State):
    docs = state.docs
    scores = []
    good_docs = []

    for d in docs:
        s = llm_evaluate_chain.invoke({
            'question': state.question,
            'chunk': d.page_content
        })
        scores.append(s.score)
        if s.score > LOWER_THRESHOLD:
            good_docs.append(d)

    if not scores:
        verdict = 'incorrect'
        reason = 'No documents retrieved'
    elif any(s > UPPER_THRESHOLD for s in scores):
        verdict = 'correct'
        reason = f'At least one document scored more than {UPPER_THRESHOLD}'
    elif all(s < LOWER_THRESHOLD for s in scores):
        verdict = 'incorrect'
        reason = f'All docs scored less than {LOWER_THRESHOLD}'
    else:
        verdict = 'ambiguous'
        reason = (f'No doc scored above {UPPER_THRESHOLD}, and not all scored '
                  f'below {LOWER_THRESHOLD}')

    return {
        'good_docs': good_docs,
        'VERDICT': verdict,
        'reason': reason
    }


# %%
# !pip install nltk

# %%
# Run this once in your environment to download the sentence tokenizer data:
# nltk.download('punkt')

# nltk.download('punkt_tab')

# %%

def split_into_sentences_nltk(paragraph: str) -> list[str]:
    if not paragraph or not paragraph.strip():
        return []
    return nltk.sent_tokenize(paragraph.strip())

# # Example usage:
# text = "Dr. Smith arrived at 8:00 a.m. He was wearing a hat! Did you see him?"
# print(split_into_sentences_nltk(text))
# # Output: ['Dr. Smith arrived at 8:00 a.m.', 'He was wearing a hat!', 'Did you see him?']

# %%
# -----------------------------
# FILTER (LLM judge)
# -----------------------------
class KeepOrDrop(BaseModel):
    keep: bool


filter_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict relevance filter.\n"
            "Return keep=true only if the sentence directly helps answer the question otherwise return keep=false.\n"
            "Use ONLY the sentence.",
        ),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ]
)

filter_chain = filter_prompt | groq_llm.with_structured_output(KeepOrDrop)


# %%
def refine_node(state: State):
    question = state.question

    if state.VERDICT == 'correct':
        docs_to_use = state.good_docs
    elif state.VERDICT == 'incorrect':
        docs_to_use = state.web_docs
    else:  # ambiguous
        docs_to_use = state.good_docs + state.web_docs

    all_chunk = "\n\n".join(chunk.page_content for chunk in docs_to_use)
    strips = split_into_sentences_nltk(all_chunk)

    kept = []
    for s in strips:
        if filter_chain.invoke({'question': question, 'sentence': s}).keep:
            kept.append(s)

    refine_context = '\n'.join(kept).strip()

    return {
        'strips': strips,
        'kept_strips': kept,
        'refine_context': refine_context
    }

# %%
class WebQuery(BaseModel):
    query: str


rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user question into a web search query composed of keywords.\n"
            "Rules:\n"
            "- Keep it short (6-14 words).\n"
            "- If the question implies recency (e.g., recent/latest/last week/last month), add a constraint like (last 30 days).\n"
            "- Do NOT answer the question.\n"
            ,
        ),
        ("human", "Question: {question}"),
    ]
)

rewrite_chain = rewrite_prompt | groq_llm.with_structured_output(WebQuery)


# %%
def rewrite_query_node(state: State):
    web_query = rewrite_chain.invoke({'question': state.question}).query
    return {'web_query': web_query}

# %%
def web_search_node(state: State):
    query = state.web_query or state.question

    if not query:
        return {"web_docs": []}

    search_tool = TavilySearch(max_results=3, search_depth="advanced")
    search_result = search_tool.invoke(query)

    web_docs = []
    for sr in search_result.get('results', []):
        title = sr.get('title', '')
        url = sr.get('url', '')
        content = sr.get('content', '')
        text = f"TITLE: {title}\n\nURL: {url}\n\nCONTENT: {content}\n"

        web_docs.append(
            Document(page_content=text, metadata={'title': title, 'url': url})
        )

    return {'web_docs': web_docs}

# %%
# -----------------------------
# Generate
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful ML tutor. Answer ONLY using the provided context.\n"
            "If the context is empty or insufficient, say: 'I don't know.'",
        ),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)


def generate_node(state: State):
    out = (answer_prompt | gpt_llm).invoke({
        "question": state.question,
        "context": state.refine_context
    })
    return {"answer": out.content}

# %%
# -----------------------------
# Routing
# CORRECT => refine
# INCORRECT / AMBIGUOUS => rewrite -> web_search -> refine -> generate
# -----------------------------
def route_after_eval(state: State) -> str:
    if state.VERDICT == "correct":
        return "refine"
    else:
        return "rewrite_query"


# %%
# -----------------------------
# Build graph
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve_node)
g.add_node("eval_each_doc", eval_each_doc_node)
g.add_node("rewrite_query", rewrite_query_node)
g.add_node("web_search", web_search_node)
g.add_node("refine", refine_node)
g.add_node("generate", generate_node)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "eval_each_doc")

g.add_conditional_edges(
    "eval_each_doc",
    route_after_eval,
    {
        "refine": "refine",
        "rewrite_query": "rewrite_query",
    },
)

g.add_edge("rewrite_query", "web_search")
g.add_edge("web_search", "refine")
g.add_edge("refine", "generate")
g.add_edge("generate", END)

app = g.compile()

app

# %%
def main():
    print("=" * 60)
    print("Corrective RAG Chatbot — type 'exit' or 'quit' to stop")
    print("=" * 60)

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ("exit", "quit", "q"):
            print("Bye bro 👋")
            break

        if not question:
            continue

        try:
            res = app.invoke({"question": question})
        except Exception as e:
            print(f"[ERROR] Something broke: {e}")
            continue

        print("\n--- DEBUG ---")
        print("VERDICT:", res.get("VERDICT"))
        print("REASON:", res.get("reason"))
        if res.get("web_query"):
            print("WEB_QUERY:", res.get("web_query"))
        print("-------------")

        print("\nAssistant:", res.get("answer"))

# %%
if __name__ == "__main__":
    main()

# %%
# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()


# eval_llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash-lite",
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# result = eval_llm.invoke('What is AI')
# print(type(result))
# print()
# print(result)
# print()
# print(result.content[0]['text'])


# %%



