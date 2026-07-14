from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os


load_dotenv()

url = 'https://github.com/langchain-ai/langchain-community/issues/674'

loader = WebBaseLoader(url)

docs = loader.load()

print(len(docs))
print()

print(docs[0].page_content)


prompt = PromptTemplate(
    template= 'Answer the following question: {question} from the following content:\n{content}',
    input_variables=['question', 'content']
)

model = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))


parser = StrOutputParser()

chain = prompt | model | parser



result = chain.invoke(
    {
        'question': 'what are the most comments talking about?', 'content': docs[0].page_content
    }
)

print("GROQ's REPLY:",result)