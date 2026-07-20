Perfect. For an AI Engineer, you **don't need to memorize every built-in tool**. There are hundreds of integrations in LangChain, and new ones are added constantly.

The important thing is understanding **how tools work**, then learning a specific tool when your project needs it.

Here's a README you can keep in your notes.

---

# 📚 LangChain Built-in Tools Cheat Sheet

## What are Built-in Tools?

Built-in tools are **pre-made tools** provided by LangChain or its integrations.

Instead of writing your own tool from scratch, you simply import one.

Example:

```python
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

search.invoke("Latest AI News")
```

---

# 1. Search Tools ⭐⭐⭐⭐⭐

Most common.

Used whenever LLM needs internet access.

Examples

* DuckDuckGo Search
* Tavily Search
* SerpAPI
* Google Search

Example

```python
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

result = search.invoke("Who invented Python?")
print(result)
```

Use cases

* AI Search Engine
* AI Research Agent
* News Agent

---

# 2. Python REPL Tool ⭐⭐⭐⭐⭐

Lets LLM execute Python code.

```python
from langchain_experimental.tools import PythonREPLTool

python = PythonREPLTool()

python.invoke("print(5 * 9)")
```

Use cases

* Data Analysis
* Mathematical calculations
* Plotting graphs
* Pandas operations

---

# 3. Shell Tool ⭐⭐⭐⭐

Runs terminal commands.

```python
from langchain_community.tools import ShellTool

shell = ShellTool()

shell.invoke("dir")
```

Linux

```python
shell.invoke("ls")
```

Use cases

* DevOps
* File management
* Automation

---

# 4. File Management Toolkit ⭐⭐⭐⭐

Manipulates local files.

Contains tools like

* Read File
* Write File
* Copy File
* Move File
* Delete File

Example

```python
from langchain_community.agent_toolkits import FileManagementToolkit

toolkit = FileManagementToolkit(root_dir="./")

tools = toolkit.get_tools()
```

Use cases

* AI File Assistant
* Document organizer

---

# 5. SQL Database Toolkit ⭐⭐⭐⭐⭐

Allows LLM to query databases.

```python
from langchain_community.agent_toolkits import SQLDatabaseToolkit
```

Can answer

> Show top 10 customers.

instead of writing SQL manually.

Use cases

* AI Database Assistant
* BI Dashboard

---

# 6. Gmail Toolkit ⭐⭐⭐⭐

Works with Gmail.

Examples

* Read emails
* Send emails
* Search emails

Example

```python
toolkit = GmailToolkit()
```

Use cases

* Email Agent
* Personal Assistant

---

# 7. Google Calendar Toolkit ⭐⭐⭐⭐

Calendar automation.

Can

* Create events
* Delete events
* List meetings

Example

```python
CalendarToolkit()
```

Use cases

Scheduling Agent

---

# 8. GitHub Toolkit ⭐⭐⭐⭐

Interact with GitHub.

Can

* Read repositories
* Create issues
* Commit code
* Open PRs

Use cases

Coding Agents

---

# 9. Requests Toolkit ⭐⭐⭐⭐⭐

Makes HTTP requests.

```python
GET

POST

PUT

DELETE
```

Example

```python
GET https://api.example.com/users
```

Useful when interacting with APIs.

---

# 10. Wikipedia Tool ⭐⭐⭐⭐

Search Wikipedia.

```python
from langchain_community.tools import WikipediaQueryRun
```

Example

```python
tool.invoke("Albert Einstein")
```

---

# 11. Arxiv Tool ⭐⭐⭐⭐

Search research papers.

```python
tool.invoke("Transformers")
```

Returns

* abstract
* authors
* publication

Perfect for AI research agents.

---

# 12. PubMed Tool ⭐⭐⭐

Medical papers.

Useful for

Medical Chatbots

Research Assistants

---

# 13. YouTube Tool ⭐⭐⭐

Search YouTube.

Useful for

Video recommendation agents.

---

# 14. Wolfram Alpha Tool ⭐⭐⭐⭐⭐

One of the strongest tools.

Can solve

* Math
* Physics
* Chemistry
* Engineering

Example

```
integrate x^2
```

---

# 15. Slack Toolkit ⭐⭐⭐

Interact with Slack.

Can

* Send messages
* Read channels

---

# 16. Jira Toolkit ⭐⭐⭐

Enterprise projects.

Can

* Create tickets
* Update tickets

---

# 17. Zapier Toolkit ⭐⭐⭐⭐

Access thousands of APIs through Zapier.

Can interact with

* Gmail
* Sheets
* Slack
* Discord
* Notion

without writing separate integrations.

---

# 18. OpenAPI Toolkit ⭐⭐⭐⭐

Turns REST APIs into tools.

Suppose company has

```
https://company.com/api
```

LLM can use it directly.

---

# 19. Vector Store Toolkits ⭐⭐⭐⭐⭐

Interact with

* Chroma
* Pinecone
* FAISS
* Weaviate
* Qdrant

Useful in

RAG systems.

---

# 20. Retriever Tool ⭐⭐⭐⭐⭐

Any retriever can itself become a tool.

```python
retriever_tool = create_retriever_tool(
    retriever,
    "pdf_search",
    "Search uploaded PDFs"
)
```

Very common in Agents.

---

# 21. Human Tool ⭐⭐⭐

Lets the agent ask the user questions.

Example

```
What's your email?
```

before continuing.

---

# 22. JSON Tool ⭐⭐⭐

Read JSON files.

Modify JSON.

Extract fields.

---

# 23. CSV Toolkit ⭐⭐⭐

Interact with CSV files.

Great for

Business data

Excel-like agents.

---

# 24. Playwright Toolkit ⭐⭐⭐⭐⭐

Browser automation.

Can

* Open websites
* Click buttons
* Fill forms
* Login

Perfect for AI Web Agents.

---

# 25. Selenium Toolkit ⭐⭐⭐⭐

Alternative browser automation.

Useful for

Legacy websites.

---

# 26. OCR / Vision Tools ⭐⭐⭐⭐

Work with

* Images
* PDFs
* OCR

Examples

Tesseract

Unstructured

---

# 27. Notion Toolkit ⭐⭐⭐⭐

Read

Write

Search

Notion pages.

---

# 28. Discord Toolkit ⭐⭐⭐

Send Discord messages.

Read channels.

---

# 29. Azure / AWS Toolkits ⭐⭐⭐⭐

Cloud automation.

Can

* Upload files
* Manage storage
* Access cloud resources

---

# 30. Pandas DataFrame Agent ⭐⭐⭐⭐⭐

One of the coolest.

```python
Create Pandas DataFrame Agent
```

Then ask

```
What's the average salary?
```

without writing pandas code.

---

# Most Important Built-in Tools (Top 10)

| Tool                     | Difficulty | Used In         |
| ------------------------ | ---------- | --------------- |
| DuckDuckGo/Tavily Search | ⭐          | Search Agents   |
| Python REPL              | ⭐          | Data Analysis   |
| SQL Toolkit              | ⭐⭐         | Database Agents |
| File Toolkit             | ⭐          | File Assistant  |
| Retriever Tool           | ⭐          | RAG             |
| Requests Toolkit         | ⭐⭐         | APIs            |
| Playwright               | ⭐⭐⭐        | Browser Agents  |
| Pandas Agent             | ⭐⭐         | Data Science    |
| Gmail Toolkit            | ⭐⭐         | Email Assistant |
| GitHub Toolkit           | ⭐⭐         | Coding Agents   |

---

# What You Should Actually Learn

For becoming an AI Engineer, this order gives you the most value:

1. ✅ Custom Tools *(Done)*
2. ✅ Tool Calling *(Done)*
3. 🔜 Agents *(Next)*
4. ReAct Agent
5. AgentExecutor
6. Memory
7. LangGraph
8. Multi-Agent Systems
9. MCP (Model Context Protocol)
10. Learn built-in tools **as needed** for projects.

At this point, you've covered the fundamentals of tools well enough. The next major leap is **Agents**, because that's where the model starts deciding **which tool to use, when to use it, and how many times to use it** without you writing the orchestration logic manually. That's the transition from "tool calling" to "agentic AI."
