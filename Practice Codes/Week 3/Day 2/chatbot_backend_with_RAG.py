import os
import sqlite3
from contextlib import asynccontextmanager

import aiosqlite
import requests

from dotenv import load_dotenv

from typing import TypedDict, Annotated

from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

from langchain_groq import ChatGroq

from langchain_community.tools import (
    DuckDuckGoSearchRun
)

from langchain_mcp_adapters.client import (
    MultiServerMCPClient
)

from langgraph.graph import (
    StateGraph,
    START,
)

from langgraph.graph.message import (
    add_messages
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)

from langgraph.checkpoint.sqlite.aio import (
    AsyncSqliteSaver
)

# ==========================================================
# RAG Imports (NEW)
# ==========================================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings


# ==========================================================
# Environment
# ==========================================================

load_dotenv()


# ==========================================================
# Database Path
# ==========================================================

DATABASE_PATH = "chatbot.db"


# ==========================================================
# RAG Config (NEW)
# ==========================================================

VECTOR_DB_DIR = "vector_store"

embeddings = FastEmbedEmbeddings()

# Cache of thread_id -> Chroma instance so we don't reopen
# the persisted store on every single call.
_vectorstores: dict[str, Chroma] = {}


# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv(
        "GROQ_API_KEY"
    ),
)


# ==========================================================
# MCP Servers
# ==========================================================

SERVERS = {

    "math": {

        "transport": "stdio",

        "command": (
            r"C:\Users\ApriZon\Desktop\MCP Testing"
            r"\Math Server\.venv\Scripts\fastmcp.exe"
        ),

        "args": [

            "run",

            (
                r"C:\Users\ApriZon\Desktop\MCP Testing"
                r"\Math Server\main.py"
            ),

        ],

    },


    "expense": {

        "transport": "stdio",

        "command": (
            r"C:\Users\ApriZon\Desktop\MCP Testing"
            r"\Expense_Server\.venv\Scripts\fastmcp.exe"
        ),

        "args": [

            "run",

            (
                r"C:\Users\ApriZon\Desktop\MCP Testing"
                r"\Expense_Server\main.py"
            ),

        ],

    },

}


mcp_client = MultiServerMCPClient(
    SERVERS
)


# ==========================================================
# Local Tools
# ==========================================================

search = DuckDuckGoSearchRun()


@tool
def get_stock_price(
    symbol: str
) -> dict:

    """
    Fetch the latest stock price
    for a symbol such as AAPL
    or TSLA.
    """

    api_key = os.getenv(
        "ALPHA_VANTAGE_API_KEY"
    )


    if not api_key:

        return {

            "error": (
                "ALPHA_VANTAGE_API_KEY "
                "is missing."
            )

        }


    url = (

        "https://www.alphavantage.co/query"

        f"?function=GLOBAL_QUOTE"

        f"&symbol={symbol}"

        f"&apikey={api_key}"

    )


    response = requests.get(

        url,

        timeout=10,

    )


    response.raise_for_status()


    return response.json()


# ==========================================================
# RAG Helper Functions (NEW)
# ==========================================================

def get_vectorstore(
    thread_id: str
) -> Chroma:

    """
    Returns (and caches) the Chroma vectorstore
    dedicated to a single conversation thread.
    """

    if thread_id not in _vectorstores:

        _vectorstores[thread_id] = Chroma(

            collection_name=f"thread_{thread_id}",

            embedding_function=embeddings,

            persist_directory=(
                f"{VECTOR_DB_DIR}/{thread_id}"
            ),

        )

    return _vectorstores[thread_id]


def ingest_pdf(

    file_path: str,

    thread_id: str,

    filename: str = None,

):

    """
    Loads a PDF, splits it into chunks, tags each
    chunk with its source filename, and adds it to
    the vectorstore belonging to this thread.

    Safe to call multiple times per thread — new
    documents are appended, not overwritten, so a
    single conversation can hold multiple uploaded
    files.
    """

    loader = PyPDFLoader(
        file_path
    )

    docs = loader.load()


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=150,

    )

    chunks = splitter.split_documents(
        docs
    )


    resolved_name = (
        filename
        or os.path.basename(file_path)
    )


    for chunk in chunks:

        chunk.metadata["source_file"] = (
            resolved_name
        )


    vs = get_vectorstore(
        thread_id
    )

    vs.add_documents(
        chunks
    )


def get_uploaded_filenames(

    thread_id: str,

):

    """
    Returns the distinct list of filenames that
    have been ingested into this thread's
    vectorstore. Used to power a "docs uploaded"
    list in the sidebar.
    """

    vs = get_vectorstore(
        thread_id
    )

    existing = vs.get()

    metadatas = existing.get(
        "metadatas",
        [],
    )


    filenames = {

        meta.get("source_file")

        for meta in metadatas

        if meta and meta.get("source_file")

    }


    return sorted(filenames)


# ==========================================================
# LangGraph State
# ==========================================================

class ChatState(
    TypedDict
):

    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    conversation_name: str


# ==========================================================
# Structured Output
# ==========================================================

class ConversationNameSchema(
    BaseModel
):

    conversation_name: str = Field(

        description=(
            "A short descriptive title "
            "for the conversation."
        )

    )


structured_llm = (
    llm.with_structured_output(
        ConversationNameSchema
    )
)


# ==========================================================
# Conversation Database
# ==========================================================

async def initialize_database():

    async with aiosqlite.connect(
        DATABASE_PATH
    ) as db:

        await db.execute(

            """
            CREATE TABLE IF NOT EXISTS
            conversations (

                thread_id TEXT PRIMARY KEY,

                title TEXT NOT NULL

            )
            """

        )

        await db.commit()


async def save_conversation_name(

    thread_id: str,

    title: str,

):

    async with aiosqlite.connect(
        DATABASE_PATH
    ) as db:

        await db.execute(

            """
            INSERT OR REPLACE INTO
            conversations (

                thread_id,

                title

            )

            VALUES (?, ?)
            """,

            (
                thread_id,
                title,
            ),

        )

        await db.commit()


async def get_conversation_name(

    thread_id: str,

):

    async with aiosqlite.connect(
        DATABASE_PATH
    ) as db:

        async with db.execute(

            """
            SELECT title

            FROM conversations

            WHERE thread_id = ?
            """,

            (
                thread_id,
            ),

        ) as cursor:

            row = await cursor.fetchone()


    if row:

        return row[0]


    return "Untitled"


async def get_all_conversations():

    async with aiosqlite.connect(
        DATABASE_PATH
    ) as db:

        async with db.execute(

            """
            SELECT

                thread_id,

                title

            FROM conversations

            ORDER BY rowid DESC
            """

        ) as cursor:

            rows = await cursor.fetchall()


    return rows


# ==========================================================
# Build Async LangGraph
# ==========================================================

async def build_graph(

    checkpointer,

    thread_id: str = None,

):

    # ------------------------------------------------------
    # Load MCP tools
    # ------------------------------------------------------

    mcp_tools = (
        await mcp_client.get_tools()
    )


    # ------------------------------------------------------
    # RAG retrieval tool (NEW)
    # ------------------------------------------------------
    # Defined inside build_graph (not top-level) so it can
    # close over the current thread_id, same pattern as
    # how mcp_tools are loaded fresh per session.

    @tool
    def retrieve_from_document(
        query: str
    ) -> str:

        """
        Search the documents the user has uploaded in
        this conversation for content relevant to their
        question. Use this whenever the user asks
        something that could be answered from an
        uploaded PDF.
        """

        if not thread_id:

            return (
                "No document uploaded for "
                "this conversation."
            )


        vs = get_vectorstore(
            thread_id
        )

        results = vs.similarity_search(

            query,

            k=4,

        )


        if not results:

            return (
                "No relevant content found "
                "in the uploaded document(s)."
            )


        return "\n\n---\n\n".join(

            f"[Source: "
            f"{d.metadata.get('source_file', 'unknown')}]"
            f"\n{d.page_content}"

            for d in results

        )


    # ------------------------------------------------------
    # Add local tools
    # ------------------------------------------------------

    tools = [

        *mcp_tools,

        search,

        get_stock_price,

        retrieve_from_document,  # NEW

    ]


    # ------------------------------------------------------
    # Bind tools to LLM
    # ------------------------------------------------------

    llm_with_tools = (
        llm.bind_tools(
            tools
        )
    )


    # ------------------------------------------------------
    # Generate title
    # ------------------------------------------------------

    async def generate_title(

        state: ChatState

    ):

        query = (
            state["messages"][0]
            .content
        )


        response = (
            await structured_llm.ainvoke(

                "Create a short descriptive "
                "conversation title from "
                "this query:\n\n"

                f"{query}"

            )
        )


        return {

            "conversation_name":

                response
                .conversation_name

        }


    # ------------------------------------------------------
    # Decide whether title exists
    # ------------------------------------------------------

    def should_generate_title(

        state: ChatState

    ):

        if state.get(
            "conversation_name"
        ):

            return "chat_node"


        return "generate_title"


    # ------------------------------------------------------
    # Main LLM node
    # ------------------------------------------------------

    async def chat_node(

        state: ChatState

    ):

        response = (

            await llm_with_tools
            .ainvoke(

                state["messages"]

            )

        )


        return {

            "messages": [

                response

            ]

        }


    # ------------------------------------------------------
    # Tool Node
    # ------------------------------------------------------

    tool_node = ToolNode(
        tools
    )


    # ======================================================
    # Create Graph
    # ======================================================

    graph = StateGraph(
        ChatState
    )


    graph.add_node(

        "generate_title",

        generate_title,

    )


    graph.add_node(

        "chat_node",

        chat_node,

    )


    graph.add_node(

        "tools",

        tool_node,

    )


    # ======================================================
    # Graph Routes
    # ======================================================

    graph.add_conditional_edges(

        START,

        should_generate_title,

        {

            "generate_title":

                "generate_title",


            "chat_node":

                "chat_node",

        },

    )


    graph.add_edge(

        "generate_title",

        "chat_node",

    )


    graph.add_conditional_edges(

        "chat_node",

        tools_condition,

    )


    graph.add_edge(

        "tools",

        "chat_node",

    )


    # ======================================================
    # Compile Graph
    # ======================================================

    chatbot = graph.compile(

        checkpointer=checkpointer

    )


    return chatbot


# ==========================================================
# Async Application Context
# ==========================================================

@asynccontextmanager

async def get_chatbot(

    thread_id: str = None,  # NEW

):

    # ------------------------------------------------------
    # Create conversation database table
    # ------------------------------------------------------

    await initialize_database()


    # ------------------------------------------------------
    # Keep AsyncSqliteSaver alive
    # ------------------------------------------------------

    async with (

        AsyncSqliteSaver
        .from_conn_string(
            DATABASE_PATH
        )

    ) as checkpointer:


        # --------------------------------------------------
        # Build graph
        # --------------------------------------------------

        chatbot = await build_graph(

            checkpointer,

            thread_id=thread_id,  # NEW

        )


        # --------------------------------------------------
        # Give chatbot to frontend
        # --------------------------------------------------

        yield chatbot