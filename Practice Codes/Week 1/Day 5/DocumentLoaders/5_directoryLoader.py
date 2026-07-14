from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

# loader = DirectoryLoader(
#     'Yoah',

#     glob='*.pdf',

#     loader_cls=PyPDFLoader
# )

loader = DirectoryLoader(
    'Yoah',

    glob='**/*.pdf', # glob="**/*" loads everything and This is called recursive loading.

    loader_cls = PyPDFLoader,

    silent_errors=True,

    use_multithreading= True
)


for doc in loader.lazy_load():
    print(doc.page_content)

# for doc in docs:
#     print(doc.page_content)
#     print()

    
