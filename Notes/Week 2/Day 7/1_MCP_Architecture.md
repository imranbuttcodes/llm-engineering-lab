Excellent. You're already understanding the architecture, but there are a few places where I'd refine the terminology because interviewers and production engineers use slightly different wording.

---

# MCP Architecture (Correct Mental Model)

```
                    ┌────────────────────────────┐
                    │        AI Application      │
                    │                            │
                    │ Cursor / Claude / VSCode  │
                    │ LangGraph Agent           │
                    └─────────────┬──────────────┘
                                  │
                                  │
                           MCP Client
                                  │
                    JSON-RPC Messages
                                  │
═══════════════════════════════════════════════
             Transport Layer
     (STDIO / HTTP / SSE / Streamable HTTP)
═══════════════════════════════════════════════
                                  │
                           MCP Server
                                  │
          ┌────────────┬──────────────┬──────────────┐
          │            │              │
       Tools      Resources       Prompts
```

---

# 1. Host

The **Host** is the application where the LLM is running.

Examples

* Cursor
* Claude Desktop
* VS Code
* Your LangGraph Agent
* Your own chatbot

The host is responsible for

* talking to the LLM
* managing conversations
* deciding when to use MCP
* owning one or more MCP clients

Think of it as the **main application**.

---

# 2. Client

This is where many beginners get confused.

The **Client is NOT the LLM.**

The client is a small communication layer that lives inside the Host.

Its only job is

> "Talk to MCP servers."

So the flow becomes

```
LLM
   ↓
Host
   ↓
Client
   ↓
Server
```

The client

* discovers tools
* discovers resources
* discovers prompts
* sends requests
* receives responses

---

# 3. Server

The MCP Server exposes capabilities.

It might expose

```
Filesystem

GitHub

Database

Weather

Slack

Docker

Browser

Google Drive

Postgres

Redis
```

Each server advertises what it can do.

---

# Why can't Host directly talk to Server?

It technically could.

But then every Host would need to know

* HTTP
* STDIO
* WebSockets
* Authentication
* Tool Discovery
* Prompt Discovery
* Resource Discovery

Instead, MCP introduces a standard protocol.

Exactly like HTTP standardized web communication.

---

# Server exposes three primitives

This is correct.

## 1. Tools

These perform actions.

Examples

```
Create File

Delete File

Run SQL

Search GitHub

Send Email

Read Folder

Execute Python
```

These change something or perform work.

---

## 2. Resources

These are read-only data sources.

Think

```
Database schema

PDF

README.md

CSV

Logs

Configuration

Git repository
```

Resources provide information.

They don't execute anything.

---

## 3. Prompts

Prompts are reusable prompt templates stored by the server.

Instead of writing

```
Summarize this repository...
```

every time,

the server can provide

```
summarize_repo
```

The Host simply asks

```
Give me prompt "summarize_repo"
```

---

# Data Layer

Exactly.

The Data Layer defines

> **How client and server understand each other.**

That language is

**JSON-RPC**

---

# JSON-RPC

Every request follows a standard structure.

Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    ...
  }
}
```

Notice

Nobody cares whether

* Python
* Java
* Rust
* Go

is running.

Everyone speaks JSON-RPC.

---

# Why JSON-RPC instead of REST?

Excellent interview question.

## Lightweight

No URLs

No HTTP verbs

Just

```
method
params
result
```

---

## Bidirectional

Both client and server can initiate communication when supported by the transport.

REST is traditionally client → server.

---

## Transport Agnostic

It works over

* STDIO
* HTTP
* WebSocket
* Named Pipes
* Unix Sockets

REST assumes HTTP.

---

## Supports Batching

Instead of

```
Request A

Request B

Request C
```

you can send

```
[A,B,C]
```

in one message.

---

## Supports Notifications

Sometimes the client doesn't care about the response.

Example

```
Log this event.
```

No response required.

---

# Transport Layer

Perfect.

The Transport Layer answers

> **How do JSON messages physically move?**

Not

"What do they contain?"

But

"How do they travel?"

---

# Local Server

Example

```
Claude Desktop
        │
        │ STDIO
        │
Filesystem MCP
```

Communication happens through

Standard Input

Standard Output

No networking.

Very fast.

---

# Remote Server

Example

```
Cursor
      │
      │ HTTP
      │
GitHub MCP Server
```

The server is somewhere else.

Communication happens over the network.

---

# Transport Modes

Historically:

* **STDIO** → Local servers
* **HTTP + SSE** → Remote servers

However, one important update:

The MCP ecosystem has been evolving toward **Streamable HTTP**, which simplifies remote communication while preserving streaming capabilities. You'll still encounter **HTTP + SSE** in many tutorials and existing implementations, but newer MCP implementations increasingly support or prefer Streamable HTTP.

So today you can think of it as:

* **Local Server → STDIO**
* **Remote Server → HTTP-based transport (commonly HTTP+SSE, increasingly Streamable HTTP)**

---

# One Thing I'd Change in Your Notes

Instead of writing:

> Host (LLM Model)

Write:

```
Host
│
├── LLM
├── MCP Client
├── Conversation
└── Agent Logic
```

The Host is **not** the LLM.

The LLM is just one component inside the Host.

---

# Interview Answer

> **Model Context Protocol (MCP) is an open standard that enables AI applications (hosts) to communicate with external systems through MCP clients and servers using JSON-RPC. Servers expose capabilities as Tools, Resources, and Prompts, while the transport layer (such as STDIO or HTTP-based transport) moves JSON-RPC messages between clients and servers.**

I'd rate your understanding so far at **8.5/10**. You're grasping the architecture well. The remaining pieces are to see **how the protocol actually works in practice**—specifically the request lifecycle (tool discovery → tool invocation → response) and then building your own MCP server. Those two steps usually make everything "click."
