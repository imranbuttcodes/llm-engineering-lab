LET'S GOOOO! 🔥

Welcome to **Day 5** (or the next major milestone). You're about to learn one of the core ideas that makes LangChain so powerful.

Up until now, we've mostly worked with **individual components**:

* ✅ Models
* ✅ Prompt Templates
* ✅ Messages
* ✅ Structured Output
* ✅ Output Parsers

Now we're going to learn how to **connect them together**.

---

# Topic: Chains in LangChain

## First, what is a Chain?

A **Chain** is simply a sequence of components connected together, where the output of one component becomes the input of the next.

Think of it like a production line in a factory.

```
Raw Material
      │
      ▼
Machine 1
      │
      ▼
Machine 2
      │
      ▼
Machine 3
      │
      ▼
Finished Product
```

LangChain works exactly the same way.

```
User Input
      │
      ▼
Prompt Template
      │
      ▼
LLM
      │
      ▼
Output Parser
      │
      ▼
Python Object
```

Every step receives something, processes it, and passes it to the next step.

---

# Haven't We Already Used Chains?

😂 Bro...

We've actually been using chains for the last two days without calling them "chains."

For example:

```python
chain = prompt | model | parser
```

That **is a chain**.

```
Prompt
   │
   ▼
Model
   │
   ▼
Parser
```

When you wrote:

```python
result = chain.invoke({
    "topic": "Python"
})
```

LangChain automatically did:

```
Input
   │
   ▼
PromptTemplate.invoke()
   │
   ▼
PromptValue
   │
   ▼
ChatGroq.invoke()
   │
   ▼
AIMessage
   │
   ▼
JsonOutputParser.invoke()
   │
   ▼
Dictionary
```

All automatically.

---

# Why Chains?

Imagine writing everything manually.

```python
prompt_value = prompt.invoke({
    "topic": "Python"
})

response = model.invoke(prompt_value)

result = parser.invoke(response)
```

Works.

But now imagine 10 steps.

```
Prompt

↓

Model

↓

Parser

↓

Translator

↓

Summarizer

↓

Sentiment Analysis

↓

Database

↓

Retriever

↓

Another Model

↓

Final Output
```

Imagine manually calling `.invoke()` every single time.

😵 It becomes messy.

Chains automate this.

---

# LCEL (LangChain Expression Language)

This is the modern way of building chains.

Instead of writing:

```python
step1 = prompt.invoke(data)

step2 = model.invoke(step1)

step3 = parser.invoke(step2)
```

We simply write

```python
chain = prompt | model | parser
```

The `|` operator means:

> Take the output of the left component and pass it as the input to the right component.

Exactly like Unix pipes.

```
Prompt
   |
Model
   |
Parser
```

---

# Visual Representation

```
User Input
      │
      ▼
PromptTemplate
      │
      ▼
Chat Model
      │
      ▼
Output Parser
      │
      ▼
Dictionary
```

---

# Everything in LangChain is a Runnable

This is one of the most important concepts.

PromptTemplate?

✅ Runnable

ChatPromptTemplate?

✅ Runnable

ChatGroq?

✅ Runnable

JsonOutputParser?

✅ Runnable

PydanticOutputParser?

✅ Runnable

StrOutputParser?

✅ Runnable

Because they're all **Runnable**, they all support methods like:

```python
.invoke()

.batch()

.stream()

.ainvoke()
```

And because they're all compatible, LangChain lets you connect them using:

```python
|
```

---

# Simple Example

```
Input

↓

PromptTemplate

↓

ChatGroq

↓

StrOutputParser

↓

String
```

Code

```python
chain = prompt | model | parser
```

One line.

---

# Bigger Example

```
Input

↓

PromptTemplate

↓

Model

↓

JsonOutputParser

↓

Python Dictionary
```

Again

```python
chain = prompt | model | parser
```

No extra code.

---

# Chain vs Component

A component performs **one task**.

Examples:

* PromptTemplate
* ChatGroq
* JsonOutputParser

A chain combines **multiple components** into a workflow.

```
Prompt
      │
      ▼
Model
      │
      ▼
Parser
```

---

# Real-Life Analogy

Imagine making tea.

Without a chain:

```
Boil water

↓

Add tea

↓

Add sugar

↓

Add milk

↓

Mix

↓

Serve
```

You manually perform each step.

With a chain:

```
Ingredients

↓

Tea Machine

↓

Tea Ready ☕
```

The machine handles the sequence for you.

---

# What You'll Learn in the "Chains" Section

Over the next topics, we'll build from simple to advanced:

```
Chains
│
├── LCEL (|)
│
├── RunnableSequence
│
├── RunnableParallel
│
├── RunnablePassthrough
│
├── RunnableLambda
│
├── RunnableBranch
│
├── assign()
│
├── bind()
│
├── batch()
│
├── stream()
│
├── ainvoke()
│
└── Building Complex AI Pipelines
```

Each of these is a building block for creating more sophisticated AI applications.

---

# 🎯 Learning Goal

By the end of the **Chains** section, you won't just know how to call an LLM—you'll know how to build complete AI workflows such as:

* 🤖 AI Chatbots
* 📄 RAG (Retrieval-Augmented Generation) pipelines
* 📚 Document Q&A systems
* 🔄 Multi-step reasoning pipelines
* 🧠 AI agents (foundation concepts)

These all rely on the same core idea you've just started learning: **connecting simple runnables into powerful chains.**
