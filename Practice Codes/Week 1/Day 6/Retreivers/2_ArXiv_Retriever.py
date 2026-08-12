import arxiv
from langchain_core.documents import Document


def arxiv_retriever(query, max_results=3):

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    documents = []

    for paper in client.results(search):

        doc = Document(

            page_content=paper.summary,

            metadata={

                "title": paper.title,

                "authors": ", ".join(
                    a.name for a in paper.authors
                ),

                "published": str(
                    paper.published
                ),

                "pdf_url": paper.pdf_url,

                "entry_id": paper.entry_id,

            },

        )

        documents.append(doc)

    return documents


docs = arxiv_retriever(
    "Large Language Models",
    max_results=2
)


for doc in docs:
    print("Page Content")
    print(doc.page_content)
    print("MetaData")
    print(doc.metadata)