from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq 


load_dotenv()


# llm1 = HuggingFaceEndpoint(
#     repo_id='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
#     task = 'text-generation',
#     huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
# )

llm2 = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen2.5-7B-Instruct',
    task = 'text-generation',
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)

model_1 = ChatGroq(model = 'llama-3.3-70b-versatile',
                   groq_api_key = os.getenv("GROQ_API_KEY"))

model_2 = ChatHuggingFace(llm = llm2)


notes_prompt = PromptTemplate(
    template='Generate the Notes from this report: {report}',
    input_variables=['report']
)

quiz_prompt = PromptTemplate(
    template = 'Generate Quiz from this report {report}',
    input_variables=['report']
)

merge_prompt = PromptTemplate(
    template='Merge Notes {notes} and quiz {quiz}',
    input_variables=['notes', 'quiz']
)


parser = StrOutputParser()

report_prompt = PromptTemplate(
    template= 'Generate a detailed report on {topic})',
    input_variables= ['topic']
)

report_chain = report_prompt | model_1 | parser

paralled_chain = RunnableParallel({
    'notes': notes_prompt | model_1 | parser,
    'quiz': quiz_prompt | model_2 | parser
})

merge_chain = merge_prompt | model_1 | parser # here we can use either model, it doens't matter


chain = report_chain | paralled_chain | merge_chain 

 

result = chain.invoke({'topic': "PCA in Machine learning"})

print("Type:",type(result))
print()
print("Result")
print()
print(result)
print()

chain.get_graph().print_ascii()
