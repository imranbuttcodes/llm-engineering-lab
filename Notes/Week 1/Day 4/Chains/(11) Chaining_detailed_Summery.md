# Chains in LangChain (LCEL) 🚀

> **Day 4 - LangChain Learning Notes**

---

# What is a Chain?

A **Chain** is a sequence of connected components where the output of one component becomes the input of the next.

Think of it like a **factory assembly line**.

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
 Final Product
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
Final Output
```

---

# Why Do We Need Chains?

Without chains:

```python
prompt = prompt_template.invoke(...)
response = model.invoke(prompt)
output = parser.invoke(response)
```

You manually execute every step.

With Chains:

```python
chain = prompt | model | parser

result = chain.invoke({...})
```

Everything happens automatically.

---

# LCEL (LangChain Expression Language)

LangChain uses **LCEL (LangChain Expression Language)**.

Instead of writing lots of code, we connect components using the **pipe operator (`|`)**.

Example

```python
chain = prompt | model | parser
```

Think of it like Linux pipes.

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

# Building Blocks of a Chain

The most common runnable components are:

```
Input
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
Final Output
```

Each block is called a **Runnable**.

Examples:

* PromptTemplate
* ChatPromptTemplate
* ChatGroq
* ChatHuggingFace
* StrOutputParser
* JsonOutputParser
* PydanticOutputParser
* RunnableParallel
* RunnableBranch
* RunnableLambda

---

# invoke()

Every chain is executed using

```python
result = chain.invoke(input)
```

Example

```python
result = chain.invoke({
    "topic":"Artificial Intelligence"
})
```

---

# Chain Graph

Every chain can visualize itself.

```python
chain.get_graph().print_ascii()
```

Example

```
Input
 │
 ▼
Prompt
 │
 ▼
LLM
 │
 ▼
Parser
 │
 ▼
Output
```

Very useful for debugging complex workflows.

---

# 1. Simple Chain

The most basic chain.

```
Input
 │
 ▼
Prompt
 │
 ▼
LLM
 │
 ▼
Parser
 │
 ▼
Answer
```

Code

```python
prompt = PromptTemplate(...)

model = ChatGroq(...)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({
    "topic":"Python"
})
```

Flow

```
Topic

↓

Prompt

↓

Model

↓

Parser

↓

String
```

Use Cases

* Chatbots
* Q&A
* Text generation
* Translation
* Summarization

---

# 2. Sequential Chain

A sequential chain contains **multiple steps**.

Output from one step becomes input to another.

Example

```
Topic

↓

Generate Report

↓

Report

↓

Generate Summary

↓

Summary
```

Code

```python
chain = (
    report_prompt
    | model
    | parser
    | summary_prompt
    | model
    | parser
)
```

Example

Input

```
PCA
```

↓

Report

↓

Summary

↓

Final Output

---

## Automatic Variable Mapping

This is one of LCEL's coolest features.

Suppose

Prompt 1 outputs

```
"This is the report..."
```

Prompt 2 expects

```python
{text}
```

LangChain automatically converts

```
"This is the report..."
```

into

```python
{
    "text":"This is the report..."
}
```

No manual work required.

---

# RunnableParallel

RunnableParallel executes multiple chains **at the same time**.

Instead of

```
Task A

↓

Task B

↓

Task C
```

everything runs simultaneously.

```
            Input
              │
      ┌───────┴────────┐
      ▼                ▼
 Notes Chain      Quiz Chain
      │                │
      └───────┬────────┘
              ▼
          Dictionary
```

Example

```python
parallel_chain = RunnableParallel({

    "notes": notes_chain,

    "quiz": quiz_chain

})
```

Output

```python
{
    "notes":"...",

    "quiz":"..."
}
```

---

# Why RunnableParallel?

Instead of waiting

```
Notes

↓

Quiz
```

both execute together.

Faster.

More scalable.

Used heavily in production AI systems.

---

# Parallel + Merge

After parallel execution, outputs can be merged.

```
           Report
              │
     ┌────────┴─────────┐
     ▼                  ▼
 Notes               Quiz
     │                  │
     └────────┬─────────┘
              ▼
         Merge Prompt
              │
              ▼
         Final Document
```

Example

```python
merge_chain = merge_prompt | model | parser

chain = report_chain | parallel_chain | merge_chain
```

---

# RunnableBranch

RunnableBranch adds **decision making**.

Instead of one path

```
Input

↓

Output
```

the chain chooses different paths.

Example

```
Feedback

↓

Classifier

↓

Positive?

↓

Yes → Positive Response

No → Negative Response
```

---

Example Code

```python
branch = RunnableBranch(

(
lambda x: x.sentiment=="positive",

positive_chain

),

(
lambda x: x.sentiment=="negative",

negative_chain

),

RunnableLambda(
lambda x:"Unknown"
)

)
```

---

Flow

```
Feedback

↓

Sentiment Analysis

↓

Positive?

├── Yes

│     ↓

│ Positive Prompt

│     ↓

│ Response

│

└── No

      ↓

Negative Prompt

      ↓

Response
```

---

# RunnableLambda

RunnableLambda allows inserting **normal Python code** inside a chain.

Example

```python
RunnableLambda(
lambda x:x.upper()
)
```

Now the chain can perform custom operations.

Examples

* String manipulation
* Calculations
* API calls
* Database operations
* File handling
* Data preprocessing
* Logging

---

Example

```
Input

↓

Python Function

↓

Prompt

↓

LLM
```

---

# Combining Everything

One workflow may contain

* Sequential execution
* Parallel execution
* Conditional execution
* Python functions

Example

```
User Query

↓

Generate Report

↓

Parallel

├── Notes

├── Quiz

└── Flashcards

↓

Merge

↓

Sentiment Check

↓

Positive?

↓

Branch

↓

Final Output
```

This is how real AI applications are built.

---

# Output Parsers in Chains

Chains can use any parser.

Example

```
Prompt

↓

Model

↓

StrOutputParser
```

or

```
Prompt

↓

Model

↓

JsonOutputParser
```

or

```
Prompt

↓

Model

↓

PydanticOutputParser
```

Parsers convert raw model responses into useful Python objects.

---

# Chain Visualization

Use

```python
chain.get_graph().print_ascii()
```

Output

```
Input

↓

Prompt

↓

LLM

↓

Parser

↓

Output
```

Helpful for

* Debugging
* Understanding workflow
* Learning LCEL
* Large pipelines

---

# Real-World Applications

### Chatbots

```
Question

↓

Prompt

↓

LLM

↓

Answer
```

---

### AI Teacher

```
Topic

↓

Generate Report

↓

Generate Summary

↓

Generate Quiz

↓

Final Notes
```

---

### Customer Support

```
Customer Feedback

↓

Sentiment Detection

↓

Positive?

↓

Different Responses
```

---

### Document Processing

```
PDF

↓

Extract Text

↓

Summarize

↓

Generate Quiz

↓

Generate Flashcards

↓

Merge
```

---

### RAG Systems

```
Question

↓

Retriever

↓

Retrieved Documents

↓

Prompt

↓

LLM

↓

Answer
```

---

# Advantages of Chains

✅ Easy to read

✅ Modular

✅ Reusable

✅ Scalable

✅ Less code

✅ Easy debugging

✅ Production-ready workflows

---

# Concepts Covered So Far

```
LangChain Chains
│
├── What is a Chain?
├── Why Chains?
├── LCEL (|)
├── invoke()
├── Graph Visualization
│
├── Simple Chain
│      ├── Prompt
│      ├── Model
│      └── Parser
│
├── Sequential Chain
│      ├── Multi-step Workflow
│      └── Automatic Variable Mapping
│
├── RunnableParallel
│      ├── Concurrent Execution
│      ├── Dictionary Output
│      └── Merge Chain
│
├── RunnableBranch
│      ├── Conditional Logic
│      ├── Positive Path
│      ├── Negative Path
│      └── Default Path
│
├── RunnableLambda
│      └── Custom Python Functions
│
├── Output Parsers
│      ├── StrOutputParser
│      ├── JsonOutputParser
│      └── PydanticOutputParser
│
└── Real-world AI Pipelines
```

---

# Key Takeaways

* A **Chain** connects multiple runnable components into a workflow.
* **LCEL (`|`)** is the simplest way to build chains.
* **Simple Chains** perform one task from input to output.
* **Sequential Chains** execute multiple steps where each output feeds the next step.
* **RunnableParallel** executes independent tasks simultaneously and returns a dictionary of results.
* **RunnableBranch** enables conditional logic by routing execution based on conditions.
* **RunnableLambda** allows you to integrate custom Python functions into a chain.
* **Output Parsers** convert raw LLM responses into structured and usable data.
* **`chain.get_graph().print_ascii()`** helps visualize and debug chain execution.
* These concepts form the foundation for advanced LangChain topics such as **RAG, AI Agents, Multi-Agent Systems, Tool Calling, and Production AI Workflows**.
