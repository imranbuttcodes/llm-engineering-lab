# from dotenv import load_dotenv
# from deepeval import evaluate
# from deepeval.test_case import LLMTestCase
# from deepeval.metrics import AnswerRelevancyMetric

# load_dotenv()

# # --- Test case 1: a good answer (should PASS) ---
# case_1 = LLMTestCase(
#     input="What is the capital of France?",
#     actual_output="The capital of France is Paris.",
# )

# # --- Test case 2: an off-topic answer (should FAIL) ---
# case_2 = LLMTestCase(
#     input="What is the capital of France?",
#     actual_output="France is a beautiful country famous for its food and wine.",
# )

# # --- One metric, judged by an LLM (pinned for reproducibility) ---
# metric = AnswerRelevancyMetric(threshold=0.7, model="gpt-4.1", include_reason=True)

# # --- Run BOTH cases through the metric, with a printed report ---
# evaluate(test_cases=[case_1, case_2], metrics=[metric])




from deepeval import evaluate
from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# 1. GROQ = OUR LLM-AS-A-JUDGE
# ============================================================

class GroqJudge(DeepEvalBaseLLM):

    def __init__(self):
        self.model = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content

    async def a_generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)
        return response.content

    def get_model_name(self):
        return "Groq Llama 3.3 70B"


judge = GroqJudge()


# ============================================================
# 2. OUR GOLDEN DATA
# ============================================================

input_question = "What is the tuition refund deadline?"

expected_output = (
    "Eligible tuition refund requests must normally be submitted "
    "within 7 calendar days of the original payment."
)


# ============================================================
# 3. WHAT OUR RETRIEVER ACTUALLY RETURNED
# ============================================================

retrieval_context = [
    "Fall 2026 tuition invoices are published in the Student Portal "
    "on August 3.",

    "Eligible tuition refund requests must normally be submitted "
    "within 7 calendar days of the original payment.",

    "The standard tuition payment deadline is August 31 at "
    "11:59 PM local time."
]


# ============================================================
# 4. RAG OUTPUT
# ============================================================

actual_output = (
    "You normally have 7 calendar days from the original payment "
    "to submit an eligible tuition refund request."
)


# ============================================================
# 5. TEST CASE
# ============================================================

test_case = LLMTestCase(
    input=input_question,
    actual_output=actual_output,
    expected_output=expected_output,
    retrieval_context=retrieval_context,
)


# ============================================================
# 6. CONTEXTUAL RECALL
# ============================================================

contextual_recall = ContextualRecallMetric(
    threshold=0.7,
    model=judge,
    include_reason=True,
)


# ============================================================
# 7. CONTEXTUAL PRECISION
# ============================================================

contextual_precision = ContextualPrecisionMetric(
    threshold=0.7,
    model=judge,
    include_reason=True,
)


# ============================================================
# 8. RUN EVALUATION
# ============================================================

evaluate(
    test_cases=[test_case],
    metrics=[
        contextual_recall,
        contextual_precision,
    ],
)