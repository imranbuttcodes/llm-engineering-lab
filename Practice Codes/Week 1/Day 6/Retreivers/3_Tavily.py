from tavily import TavilyClient
from dotenv import load_dotenv
import os
from langchain_core.documents import Document


load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
response = tavily_client.search(
    'Latest News On Amazon Hiring Engineers instead of using AI!',
    max_results= 3
)

# print(type(response))
# print(response.keys())
# print(response['results'][0])

documents = []


for result in response["results"]:

    doc = Document(

        page_content=result["content"],

        metadata={

            "title": result["title"],

            "url": result["url"]

        }

    )

    documents.append(doc)


print("Latest News On Amazon Hiring Engineers instead of using AI!")
for doc in documents:
    print(doc.page_content)
    print()
    