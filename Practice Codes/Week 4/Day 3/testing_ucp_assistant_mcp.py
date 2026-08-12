import os
import asyncio
from typing import Literal
from dotenv import load_dotenv

# LangChain / LangGraph imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# The official LangChain MCP adapter!
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables (for GROQ_API_KEY)
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise Exception("ERROR: GROQ_API_KEY must be set in your .env file to use ChatGroq!")

# ==========================================
# ASYNC AGENT LOOP USING MCP ADAPTERS
# ==========================================

SERVERS = {
    "ucp_portal": {
        "transport": "stdio",
        "command": "python",
        "args": [
            "C:\\Users\\ApriZon\\Desktop\\Testing PlayWright\\mcp_server.py"
        ],
        "env": os.environ.copy()
    }
}

async def main():
    print("\n" + "="*60)
    print("🔌 Booting MCP Client (via langchain_mcp_adapters)...")
    print("="*60)
    
    # As of langchain-mcp-adapters 0.1.0, MultiServerMCPClient is NOT a context manager.
    client = MultiServerMCPClient(SERVERS)
    
    # 🤯 The adapter handles all the dynamic JSON schema to Pydantic conversion for us!
    # Note: This is an async call!
    langchain_tools = await client.get_tools()
    
    print(f"✅ Connected! Dynamically discovered {len(langchain_tools)} tools:")
    for t in langchain_tools:
        print(f"  - {t.name}")
        
    # ==========================================
    # INITIALIZE LLM & BUILD LANGGRAPH
    # ==========================================
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    llm_with_tools = llm.bind_tools(langchain_tools)
    
    system_prompt = """You are a highly intelligent AI assistant for students at the University of Central Punjab (UCP).
    You have access to live data via remote MCP scraping tools. 
    When a student asks a question, autonomously use the tools to fetch the required information and present it cleanly.
    If a tool fails because credentials are missing, ask the user for their UCP email and password, and use the set_credentials tool to save them.
    Be concise, friendly, and format your output beautifully in markdown."""
    
    def agent_node(state: MessagesState):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"
        
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(langchain_tools))
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    print("\n🎓 UCP AI Agent is Ready! Type 'exit' to stop.\n")
    config = {"configurable": {"thread_id": "ucp_session_mcp"}}
    
    # Chat Loop
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        if not user_input.strip():
            continue
            
        print("\nAgent is thinking...", flush=True)
        
        # Stream async
        async for event in app.astream(
            {"messages": [HumanMessage(content=user_input)]}, 
            config=config, 
            stream_mode="values"
        ):
            msg = event["messages"][-1]
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_name = msg.tool_calls[0]['name']
                print(f"  [📡 MCP Server Executing: {tool_name}...]")
            final_message = msg
            
        if final_message and hasattr(final_message, "content"):
            print(f"\nAgent:\n{final_message.content}\n")

if __name__ == "__main__":
    asyncio.run(main())
