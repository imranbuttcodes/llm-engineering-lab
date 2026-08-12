from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

loader = TextLoader('cricket.txt', encoding='utf-8')

docs = loader.load()


model = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    groq_api_key = os.getenv('GROQ_API_KEY')
)

prompt = PromptTemplate(
    template= 'Generate a 2 line Funniest possible summery of {topic}',
    input_variables= ['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({
    'topic': docs[0].page_content
})


print(result)

# print(type(docs))
# print(docs)
# print()
# print(type(docs[0]))
# print()
# print("YOAH")
# print(docs[0])
# print()
# print(type(docs[0].page_content))
# print()
# print(docs[0].metadata)
