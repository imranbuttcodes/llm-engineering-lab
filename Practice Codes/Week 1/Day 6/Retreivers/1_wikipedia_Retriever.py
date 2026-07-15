# from langchain_community.retrievers import WikipediaRetriever

# retriever = WikipediaRetriever(
#     top_k_results=2,
#     doc_content_chars_max=1200
# )

# docs = retriever.invoke("Machine Learning")

# for i, doc in enumerate(docs, start=1):
#     print("=" * 60)
#     print(f"Document {i}")
#     print("=" * 60)

#     print(doc.page_content)

#     print("\nMetadata:")
#     print(doc.metadata)

import requests

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "titles": "Machine Learning"
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.text[:500])