BRO 🔥

You've now reached another important concept in LangChain: **Toolkits**.

Your code is correct, but let's understand **why Toolkits exist**, because right now it probably feels like:

> "Why not just pass `[add, multiply]` directly?"

Exactly. For **two tools**, a toolkit seems unnecessary. Its real value appears when you have many related tools.

---

# What you wrote

```python
@tool
def add(...):
    ...

@tool
def multiply(...):
    ...
```

Then

```python
class MathToolkit:

    def get_tools(self):
        return [add, multiply]
```

Then

```python
toolkit = MathToolkit()

tools = toolkit.get_tools()
```

Perfect.

---

# Why Toolkits?

Imagine you're building an AI assistant that works with Gmail.

Without a toolkit:

```python
gmail_tools = [
    send_email,
    read_email,
    search_email,
    delete_email,
    archive_email,
    draft_email,
    reply_email,
    forward_email,
]
```

Now imagine another file needs these.

You'd have to import all eight tools again.

Instead

```python
gmail_toolkit = GmailToolkit()

tools = gmail_toolkit.get_tools()
```

Done.

---

# Think of it like a toolbox

Instead of carrying

```
🔨 Hammer

🪛 Screwdriver

🔧 Wrench

🪚 Saw
```

one by one,

you carry

```
🧰 Toolbox
```

Open it whenever you need.

That's literally what a Toolkit is.

---

# Another Example

Database Toolkit

```python
class SQLToolkit:

    def get_tools(self):

        return [

            execute_query,

            list_tables,

            describe_table,

            insert_row,

            update_row,

            delete_row,
        ]
```

Now

```python
tools = SQLToolkit().get_tools()
```

instead of

```python
tools = [
    execute_query,
    list_tables,
    describe_table,
    insert_row,
    update_row,
    delete_row,
]
```

Cleaner.

---

# Production Example

LangChain itself has toolkits.

For example

```
SQLDatabaseToolkit

GmailToolkit

SlackToolkit

GitHubToolkit

Office365Toolkit
```

Each one bundles together a related set of tools.

---

# Why not just use a list?

You absolutely can.

For small projects

```python
tools = [add, multiply]
```

is perfectly fine.

A Toolkit becomes valuable when:

* You have many related tools.
* You want to package them as a reusable component.
* Different projects can import the entire toolkit instead of individual tools.
* The toolkit may create or configure tools internally (for example, using a shared database connection or API client).

---

# One small improvement

I'd write it like this:

```python
class MathToolkit:

    @staticmethod
    def get_tools():
        return [
            add,
            multiply,
        ]
```

Now you don't even need to create an object:

```python
tools = MathToolkit.get_tools()
```

Or, if the toolkit needs configuration (API keys, database connections, etc.), then keeping it as an instance like you wrote is the better choice.

---

# Where we are now

You've completed the **Tools** chapter:

* ✅ `@tool`
* ✅ `StructuredTool`
* ✅ `BaseTool`
* ✅ Multiple Tool Calling
* ✅ Toolkits

The next big chapter is **Agents**, where you'll finally stop manually managing `tool_calls` and `ToolMessage`s and let the framework handle the reasoning-and-tool-execution loop automatically. That's where everything you've learned so far comes together. 🚀
