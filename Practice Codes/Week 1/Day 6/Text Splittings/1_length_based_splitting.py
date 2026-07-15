from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

text = """
Python is one of the most popular programming languages.

It is used in AI.

It is used in Web Development.

It is used in Data Science.
"""




splitter = CharacterTextSplitter(
    separator='\n\n',
    chunk_size = 50,
    chunk_overlap = 10
)


# chunks = splitter.split_text(text)

# print(type(chunks))
# print(chunks)

loader = PyPDFLoader('dl-curriculum.pdf')


docs = loader.load()



from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(
    model = 'llama-3.3b-70b-versatile',
    groq_api_key = os.getenv('GROQ_API_KEY')
)


prompt = PromptTemplate(
    template='Generate a Summery on the following Content:\n\n{content}',
    input_variables= ['content']
)



chunks = splitter.split_documents(docs)

print(len(chunks))

print(chunks[0].page_content)
print()
print()
print(docs[0].page_content)
print()
print()
print()
print(docs[0])

