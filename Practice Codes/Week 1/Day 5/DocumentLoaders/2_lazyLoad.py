from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

loader = TextLoader('cricket.txt', encoding='utf-8')

docs = loader.lazy_load()
for doc in docs:
    print(doc.page_content)