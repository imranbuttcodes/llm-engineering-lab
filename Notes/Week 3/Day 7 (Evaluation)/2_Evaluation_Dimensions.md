This is actually one of the **most important concepts in LLM evaluation**, and many people confuse these terms. Let's break them down carefully.

---

# Evaluation Dimensions

Think of evaluation dimensions as **different ways to judge an answer**.

Suppose the user asks:

> **"Who founded Microsoft?"**

The model answers:

> "Microsoft was founded by Bill Gates and Paul Allen."

Now let's judge this answer from different perspectives.

---

# 1. Correctness (Accuracy)

> **Is the answer factually correct?**

Question:

> Who founded Microsoft?

Answer:

> Bill Gates and Paul Allen

✅ Correct

---

Question:

> Who founded Microsoft?

Answer:

> Elon Musk

❌ Incorrect

---

Correctness ignores **where the information came from**.

It only asks:

> Is it true?

---

# 2. Faithfulness

This one is **ONLY used when context is provided.**

Imagine RAG.

Retrieved Context:

```text
Microsoft was founded in 1975 by Bill Gates and Paul Allen.
```

LLM Answer:

```text
Microsoft was founded by Bill Gates and Paul Allen.
```

Everything came from the context.

✅ Faithful

---

Now suppose:

Retrieved Context:

```text
Microsoft was founded by Bill Gates and Paul Allen.
```

LLM says:

```text
Microsoft was founded by Bill Gates, Paul Allen and Steve Jobs.
```

Steve Jobs wasn't in the context.

❌ Not Faithful

---

## Definition

Faithfulness asks:

> **Did the model invent information not supported by the provided context?**

It doesn't care whether the invented information is true or false.

It only asks:

> Did you stay faithful to the retrieved evidence?

---

# 3. Groundedness

Groundedness is very close to faithfulness, but slightly broader.

Groundedness asks:

> **Can every important claim be traced back to evidence?**

Example:

Context:

```text
Bill Gates and Paul Allen founded Microsoft.
```

Answer:

```text
Microsoft was founded by Bill Gates and Paul Allen.
```

Every sentence is supported.

✅ Grounded

---

Answer:

```text
Bill Gates founded Microsoft because he wanted to compete with Apple.
```

Context never mentioned Apple.

So the second claim is unsupported.

❌ Not Grounded

---

## Difference

Faithfulness:

> Don't hallucinate beyond the context.

Groundedness:

> Every claim must be backed by evidence.

Most RAG papers use them almost interchangeably nowadays, but technically:

* **Faithfulness** focuses on hallucination relative to the supplied context.
* **Groundedness** focuses on evidence support for each claim.

---

# Simple Analogy

Imagine writing a research paper.

Teacher gives you three references.

Faithfulness:

> Did you invent something not written in those references?

Groundedness:

> Can you cite a reference for every statement?

---

# 4. Relevance

Suppose user asks:

> How to reverse a linked list?

Answer:

```text
Python was created by Guido van Rossum.
```

Correct?

Yes.

Helpful?

No.

Relevant?

❌ No.

---

# 5. Answer Relevancy

This asks:

> Does the answer actually answer the user's question?

Example:

Question:

> What is AI?

Answer:

```text
AI stands for Artificial Intelligence.
```

✅ Relevant

---

Question:

> What is AI?

Answer:

```text
Artificial Intelligence was invented in 1956.
```

Partially relevant.

Question not fully answered.

---

# 6. Context Relevance

Specific to RAG.

Retrieved Documents:

```
Document 1

AI definition.

Document 2

Football World Cup.

Document 3

Cats.
```

User asked about AI.

Only Document 1 matters.

Documents 2 and 3 are irrelevant.

Poor retrieval.

---

# 7. Context Precision

Measures:

> How much retrieved context was actually useful?

Retrieve 100 documents.

Only 3 matter.

Very low precision.

Retrieve 3 documents.

All useful.

Very high precision.

---

# 8. Context Recall

Measures:

> Did retrieval fetch **all** the necessary information?

Question:

> Tell me Microsoft's founders and founding year.

Retriever only finds:

```
Bill Gates
Paul Allen
```

Missing:

```
1975
```

Low recall.

---

# 9. Completeness

Question:

> Explain TCP/IP.

Answer:

```text
TCP/IP is a protocol.
```

Correct?

Yes.

Complete?

No.

---

Good answer:

```text
TCP/IP is the Internet protocol suite consisting of TCP and IP. TCP provides reliable communication while IP handles addressing and routing.
```

Complete.

---

# 10. Helpfulness

Suppose user asks:

> Explain recursion.

Answer:

```
Recursion is recursion.
```

Technically correct?

Maybe.

Helpful?

No.

---

Better:

```
Recursion is when a function calls itself until a base condition is reached.
```

Helpful.

---

# 11. Coherence

Does the answer make logical sense?

Bad:

```
Microsoft was founded yesterday because recursion.
```

Correct?

No.

Coherent?

Definitely not.

---

# 12. Fluency

Grammar.

Example:

```
AI are computer make human.
```

Low fluency.

---

# 13. Conciseness

Question:

> What is Python?

Answer:

40 pages.

Correct?

Yes.

Concise?

No.

---

# 14. Hallucination Rate

How often does the model invent facts?

Lower is better.

---

# Big Picture

| Dimension          | What it measures                                           |
| ------------------ | ---------------------------------------------------------- |
| Correctness        | Is it factually correct?                                   |
| Faithfulness       | Does it avoid inventing facts beyond the provided context? |
| Groundedness       | Can every important claim be supported by evidence?        |
| Relevance          | Is the response about the user's question?                 |
| Answer Relevancy   | Does it directly answer the question?                      |
| Context Relevance  | Were the retrieved documents relevant?                     |
| Context Precision  | How much retrieved context was actually useful?            |
| Context Recall     | Did retrieval find all needed information?                 |
| Completeness       | Is the answer sufficiently complete?                       |
| Helpfulness        | Is the explanation genuinely useful?                       |
| Coherence          | Is it logically consistent?                                |
| Fluency            | Is the language natural and grammatically correct?         |
| Conciseness        | Is it appropriately brief?                                 |
| Hallucination Rate | How often does it fabricate unsupported information?       |

---

## For Nexus AI

You'll mainly evaluate these dimensions:

* **General Chat:** Correctness, Helpfulness, Relevance, Coherence.
* **RAG:** Faithfulness, Groundedness, Context Precision, Context Recall, Answer Relevancy.
* **Agents:** Tool Selection Accuracy, Task Completion Rate, Planning Quality, Efficiency.
* **Security:** Prompt Injection Resistance, Jailbreak Resistance, Tool Misuse Prevention.

These cover the vast majority of production evaluation you'll perform on a system like Nexus AI.
