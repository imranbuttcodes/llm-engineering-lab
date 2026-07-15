from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Machine Learning is a field of AI.

It includes supervised learning.

It includes unsupervised learning.

Principal Component Analysis reduces dimensions.
"""


# Default Seperator Order

# [
#     "\n\n",   # Paragraph
#     "\n",     # Line
#     " ",      # Space
#     ""        # Character
# ]

# Custom Seprator


# splitter = RecursiveCharacterTextSplitter(
#     separators=[
#         "\n\n",
#         "\n",
#         ". ",
#         " ",
#         ""
#     ],
#     chunk_size=300,
#     chunk_overlap=50
# )

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("Chunk Len:",len(chunk))
    print("-"*40)