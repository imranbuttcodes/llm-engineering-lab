from langchain_text_splitters import TokenTextSplitter

text = """
Machine Learning is one of the most important fields of Artificial Intelligence.
It is widely used in healthcare, finance, robotics, and autonomous vehicles.
"""

splitter = TokenTextSplitter(
    chunk_size=20, # here chunk_size means characters, 
    chunk_overlap=5
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}")
    print(chunk)
    print("-"*40)