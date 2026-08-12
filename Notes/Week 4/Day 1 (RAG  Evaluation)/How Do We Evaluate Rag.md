## How do you evaluate your RAG chatbot?

1. **Build an Evaluation Suite:**
   I don't just perform one test; I build an evaluation suite that tests the application at three distinct levels:

   * **Component Level:** Evaluate the retriever using precision/recall and evaluate the generator in isolation.
   * **Pipeline Level:** Use the **RAG Triad** — Context Relevance, Faithfulness, and Answer Relevance.
   * **Application Level:** Evaluate correctness, completeness, tone, safety (PII, jailbreaks), and operational metrics such as latency and cost.

2. **Implement Regression Testing:**
   I run this evaluation suite to compare new versions against a baseline. There are three depths of regression testing:

   * Basic manual comparison
   * Using experiment tracking tools such as MLflow
   * Full CI/CD integration with automated release gates

3. **Online Evaluation:**
   Evaluation continues after deployment. I track live performance, capture user feedback such as thumbs up/down, monitor for drift, and create a self-improving loop where mistakes in production are used to enrich the offline **golden evaluation dataset**.

This framework demonstrates professional, end-to-end experience with RAG systems rather than just knowing a few isolated evaluation metrics.
