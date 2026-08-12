from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate

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

prompt1 = template_1.invoke({'topic': 'black hole'})  

result_1 = model.invoke(prompt1)

prompt2 = template_2.invoke({'text': result_1.content})


print(result_1.content)

print()
print()
result2 = model.invoke(prompt2)
print("Summery:")
print(result2.content)