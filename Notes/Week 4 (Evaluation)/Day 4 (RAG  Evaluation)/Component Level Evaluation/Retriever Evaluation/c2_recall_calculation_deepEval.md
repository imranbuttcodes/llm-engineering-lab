## Contextual Recall — LLM-as-a-Judge

Contextual recall evaluates whether the **retrieved chunks contain the necessary information to support the ideal answer**.

### Evaluation Process

1. **Breakdown into Claims**
   The LLM takes the **ideal answer** and breaks it down into individual, **atomic claims**.

2. **Context Verification**
   The LLM scans the **retrieved chunks** and checks which of those specific claims are present and supported by the retrieved context.

3. **Scoring**
   Calculate recall as:

[
\text{Contextual Recall} =
\frac{\text{Claims found in retrieved context}}
{\text{Total atomic claims from ideal answer}}
]

**Example:**
If the ideal answer contains **2 atomic claims**, and the retrieved context supports **1** of them:

[
\text{Recall} = \frac{1}{2} = 50%
]

So, **contextual recall measures how much of the information needed to produce the ideal answer was actually retrieved.**
