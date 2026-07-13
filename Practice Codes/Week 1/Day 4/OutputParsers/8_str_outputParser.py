from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  StrOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = 'Qwen/Qwen2.5-7B-Instruct',
    task = 'text-generation',
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)


model = ChatHuggingFace(llm=llm)

# detailed report

template_1 = PromptTemplate.from_template('Write a detailed Report on {topic}')

template_2 = PromptTemplate.from_template('Write a 5 line summery on the following:\n {text}')

parser = StrOutputParser()

chain = template_1 | model | parser | template_2 | model | parser

result = chain.invoke({'topic': 'black hole'})

print(result)