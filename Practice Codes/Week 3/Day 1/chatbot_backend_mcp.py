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
# Environment
# ==========================================================

load_dotenv()


# ==========================================================
# Database Path
# ==========================================================

DATABASE_PATH = "chatbot.db"


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
    checkpointer
):

    # ------------------------------------------------------
    # Load MCP tools
    # ------------------------------------------------------

    mcp_tools = (
        await mcp_client.get_tools()
    )


    # ------------------------------------------------------
    # Add local tools
    # ------------------------------------------------------

    tools = [

        *mcp_tools,

        search,

        get_stock_price,

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

async def get_chatbot():

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

            checkpointer

        )


        # --------------------------------------------------
        # Give chatbot to frontend
        # --------------------------------------------------

        yield chatbot