from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
import sqlite3
import requests
from dotenv import load_dotenv
import os


# Note: we only need to run it once.
# Create our Own Table
#   |
#   |

# conn = sqlite3.connect(
#     "chatbot.db",
#     check_same_thread=False
# )

# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS conversations(
#     thread_id TEXT PRIMARY KEY,
#     title TEXT NOT NULL
# )
# """)

# conn.commit()

load_dotenv()

llm = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    api_key = os.getenv("GROQ_API_KEY")
)




# ---------------- Tools ------------------------

search = DuckDuckGoSearchRun()

@tool 
def calculator(a: int, b: int, operation: str) -> int | float:
    """Perform basic arithmetic operations: add, subtract, multiply, or divide."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
    else:
        raise ValueError(f"Unsupported operation: {operation}")


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()


tools = [search, calculator, get_stock_price]


llm_with_tools = llm.bind_tools(tools=tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    conversation_name: str

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


class ConversationNameSchema(BaseModel):
    conversation_name: str = Field(description = 'A short title for the conversation')


structured_llm = llm.with_structured_output(ConversationNameSchema)

def generate_title(state: ChatState):
    query = state['messages'][0].content
    response = structured_llm.invoke(f"Suggest a short conversation Name from the following query:\n\nquery: {query}")


    return {
        'conversation_name': response.conversation_name
    }


def should_generate_title(state: ChatState):
    if (state.get('conversation_name')):
        return 'end'
    else:
        return 'generate'



"""
This node(ToolNode) is responsible for

finding which tool the LLM requested
executing it
putting the ToolMessage back into state
"""    
tool_node = ToolNode(tools)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node('tools', tool_node)
graph.add_node("generate_title", generate_title)


#graph.add_edge(START, "chat_node")
graph.add_conditional_edges(START, 
                            should_generate_title,
                            {
                                'end': 'chat_node',
                                'generate': 'generate_title'
                            })
graph.add_edge('generate_title', 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition) # returns exactly END or tools
graph.add_edge('tools', 'chat_node')
#graph.add_edge("chat_node", END)

# Checkpointer

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

chatbot = graph.compile(checkpointer=checkpointer)

# response = chatbot.invoke(
#     {
#         'messages': HumanMessage(content='What is my Name?')
#     },
#     config = {
#         'configurable': {
#             'thread_id': '1'
#         }
#     }
# )

# print(response)


def save_conversation_name(thread_id: str, title: str):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO conversations
        (thread_id, title)
        VALUES (?, ?)
        """,
        (thread_id, title)
    )

    conn.commit()



def get_conversation_name(thread_id: str):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title
        FROM conversations
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return "Untitled"



def get_all_conversations():

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT thread_id, title
        FROM conversations
        ORDER BY rowid DESC
        """
    )

    return cursor.fetchall()


