from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os



load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a Detailed Report bout {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a short summery of topic: {text}',
    input_variables=['text']
) 
#
#Qwen/Qwen2.5-7B-Instruct
llm = HuggingFaceEndpoint(
    repo_id = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
    task = 'text-generation',
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)   


model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic':'2005 Flood in pakistan'})

print(result)

chain.get_graph().print_ascii()
#chain.get_graph().draw_png()

