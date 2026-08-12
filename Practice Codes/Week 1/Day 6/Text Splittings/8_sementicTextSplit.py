from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

text = """
Machine Learning is a field of AI.

Random Forest is a supervised algorithm.

Neural Networks are powerful.

Pizza originated in Italy.

Pepperoni is delicious.
"""

splitter = SemanticChunker(
    HuggingFaceEmbeddings(model = 'sentence-transformers/all-MiniLM-L6-v2')
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print(chunk)