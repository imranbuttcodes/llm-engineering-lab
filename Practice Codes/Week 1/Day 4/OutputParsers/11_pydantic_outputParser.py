from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = 'Qwen/Qwen2.5-7B-Instruct',
    task = 'text-generation',
    huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)   


model = ChatHuggingFace(llm=llm)

class Book(BaseModel):
    title: str = Field(max_length=300, description="Title of the Book")
    author: str = Field(description= "Name of the Auther")
    difficulty: str = Field(description='Difficulty Level')
    chapters: list[str] = Field(description="Names of the Chapters")

parser = PydanticOutputParser(pydantic_object=Book)


print("Format Instructions:\n")
print(parser.get_format_instructions())
print('\n')


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


# prompt = prompt.invoke({'topic':'BollyWood'})

# result = model.invoke(prompt)

# result = parser.parse(result.content)

# print(type(result))
# print(result.title)
# print(result.author)
# print(result.chapters)
# print(result.difficulty)

#Using chaining

chain = prompt | model | parser

result = chain.invoke({'topic': 'AGI'})


print(type(result))
print(result.title)
print(result.author)
print(result.chapters)
print(result.difficulty)

# JsonOutputParser() Returns a Python dictionary (dict).
#  while PydanticOutputParser
# Returns an instance of your Pydantic model.