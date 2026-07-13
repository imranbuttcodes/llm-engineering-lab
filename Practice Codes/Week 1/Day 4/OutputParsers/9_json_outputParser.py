from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = 'Qwen/Qwen2.5-7B-Instruct',
    task = 'text-generation',
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)


model = ChatHuggingFace(llm=llm)

parser = JsonOutputParser()

# template1 = PromptTemplate(
#     template="""Answer the following question
#     {format_instructions}

#     Question 
#     {question}
#     """,
#     input_variables=['question'],
#     partial_variables={
#         'format_instructions': parser.get_format_instructions()
#     }
# )

# chain = template1 | model | parser

# result = chain.invoke({'question': 'What the hell is AI?'})

# print(type(result))

# print(result)


class Book(BaseModel):
    title: str = Field(description="Title of the Book")
    author: str = Field(description= "Name of the Auther")
    difficulty: str = Field(description='Difficulty Level')
    chapters: list[str] = Field(description="Names of the Chapters")

parser = JsonOutputParser(pydantic_object=Book)

print((parser.get_format_instructions()))
print()

prompt = PromptTemplate(
    template="""
    Generate a programming book 
    {format_instructions}

    topic:
    {topic}
""",
    input_variables=['topic'],
    partial_variables= {
        'format_instructions': parser.get_format_instructions()
    }
)


prompt = prompt.invoke({'topic' : 'black hole'})

result = model.invoke(prompt)

print()
print()
result = parser.parse(result.content)
print(result)
print()
print()
print(type(result))
print("Title:",result['title'])
print("Auther:",result['author'])
print("Difficulty:",result['difficulty'])
print("Chapters:",result['chapters'])


#Now using chaining
# chain = prompt | model | parser


# result = chain.invoke({'topic': 'black Hole'})

# print(type(result))
# print(result)



# JsonOutputParser() Returns a Python dictionary (dict).
#  while PydanticOutputParser
# Returns an instance of your Pydantic model.