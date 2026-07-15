from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# Python

Python is a programming language.

## Variables

Variables store values.

## Loops

Loops execute code repeatedly.

### For Loop

Example of for loop.
"""

headers = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers
)

docs = splitter.split_text(markdown_text)

for doc in docs:
    print("=" * 50)
    print(doc.page_content)
    print(doc.metadata)