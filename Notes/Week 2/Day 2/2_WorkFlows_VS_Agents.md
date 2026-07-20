BROOOOO!! 🔥

This is probably **the MOST IMPORTANT concept** before learning LangGraph.

People confuse **Workflows** and **Agents** all the time.

Let's fix that forever.

---

# Think of it like this

## Workflow = Fixed Recipe 🍳

A workflow already knows every step.

```text
1. Get PDF
2. Split PDF
3. Create Embeddings
4. Search Chroma
5. Send Context to LLM
6. Return Answer
```

Every user...

```
↓

Step 1

↓

Step 2

↓

Step 3

↓

Step 4

↓

Step 5

↓

Done
```

No thinking.

No decisions.

No choosing.

It simply follows instructions.

---

Example

Your PDF Chatbot is a **workflow**.

```
Upload PDF

↓

Load PDF

↓

Split

↓

Embed

↓

Store

↓

Retrieve

↓

LLM

↓

Answer
```

No matter what the user asks...

It ALWAYS follows this pipeline.

---

# AI Agent = Decision Maker 🧠

Now imagine:

User:

> "What's the weather in Lahore?"

The AI thinks...

```
I don't know.

↓

Need Weather Tool.

↓

Call Weather Tool.

↓

Read Result.

↓

Answer User.
```

---

Now another user says

> "What's 183 × 927?"

Agent thinks

```
Don't use Weather.

↓

Need Calculator.

↓

Call Calculator.

↓

Answer.
```

---

Now another asks

> "Summarize this PDF."

Agent thinks

```
Need RAG.

↓

Retrieve Documents.

↓

LLM.

↓

Answer.
```

Notice?

The steps changed.

---

# Workflow

```text
User

↓

A

↓

B

↓

C

↓

D

↓

E
```

Always.

---

# Agent

```text
User

↓

Think

↓

Which Tool?

↓

Use Tool

↓

Observe

↓

Need another tool?

↓

Think Again

↓

Answer
```

Different every time.

---

# Biggest Difference

Workflow

> "I already know what to do."

Agent

> "I need to figure out what to do."

That's literally the difference.

---

# Real Example

Imagine you're building CtrlCode.

## Workflow Version

User uploads GitHub repo.

```
Clone Repo

↓

Run Semgrep

↓

Run Bandit

↓

Generate Report

↓

Done
```

Every repository...

Same pipeline.

---

## Agent Version

User uploads repo.

Agent thinks...

```
Python project?

↓

Run Bandit.

↓

Wait...

I also found Docker.

↓

Run Docker Scanner.

↓

Hmm...

I found package.json.

↓

Run npm audit.

↓

Now summarize.

↓

User asks follow-up.

↓

Open vulnerable file.

↓

Explain vulnerability.

↓

Suggest patch.
```

Did you notice?

Nobody programmed that sequence.

The LLM decided it.

---

# Another Analogy

Workflow = GPS Route

```
Home

↓

Left

↓

Right

↓

Straight

↓

Destination
```

Never changes.

---

Agent = Human Driver

```
Traffic?

↓

Take another road.

↓

Road closed?

↓

Use Google Maps.

↓

Gas low?

↓

Stop at station.

↓

Continue.
```

The driver adapts.

---

# Comparison

| Workflow                   | AI Agent                   |
| -------------------------- | -------------------------- |
| Fixed steps                | Dynamic steps              |
| No reasoning               | Uses reasoning             |
| No planning                | Plans                      |
| Deterministic              | Adaptive                   |
| Easy to predict            | Behavior changes with task |
| Great for repetitive tasks | Great for open-ended tasks |
| Faster                     | More flexible              |
| Usually cheaper            | Usually more expensive     |

---

# Where does LangGraph fit?

Here's the cool part.

LangGraph can build **both**.

Workflow

```
Load PDF

↓

Split

↓

Embed

↓

Retrieve

↓

Answer
```

Agent

```
Think

↓

Use Tool

↓

Think Again

↓

Use Another Tool

↓

Need Human?

↓

Continue

↓

Answer
```

LangGraph is just the engine.

Whether you build a workflow or an agent depends on how you design the graph.

---

# The Golden Rule

I want you to remember this sentence because it'll make the rest of Week 2 much easier:

> **A workflow executes a predefined sequence of steps, while an AI agent decides what sequence of steps to execute in order to achieve a goal.**

That single idea is the foundation of modern agentic AI. Once you understand it, frameworks like LangGraph, CrewAI, OpenAI Agents SDK, and AutoGen all become much easier to grasp. 🚀
