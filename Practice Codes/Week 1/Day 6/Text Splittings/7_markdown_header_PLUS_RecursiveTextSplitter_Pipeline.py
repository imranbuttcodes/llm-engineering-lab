from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)



markdown = """
# Machine Learning

Machine Learning is a field of Artificial Intelligence.

## Supervised Learning

Supervised Learning uses labeled data.

Algorithms include:
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest

## Unsupervised Learning

Unsupervised Learning uses unlabeled data.

Algorithms include:
- PCA
- K-Means
- DBSCAN

## Reinforcement Learning

Reinforcement Learning is based on rewards and punishments.
"""



# Step 1: Split by Markdown headers
header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "H1"),
        ("##", "H2"),
    ]
)

docs = header_splitter.split_text(markdown)

# Step 2: Split large sections into smaller chunks
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = recursive_splitter.split_documents(docs)

print(f"Header Documents: {len(docs)}")
print(f"Final Chunks: {len(chunks)}")

print("Header Docs:\n", docs)
print()
print()
print("Final Chunks:\n", chunks)