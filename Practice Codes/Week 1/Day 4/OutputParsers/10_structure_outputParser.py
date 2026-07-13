from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate

from langchain.output_parsers import (
    StructuredOutputParser,
    ResponseSchema
)

load_dotenv()

# -------------------------------
# Create Response Schemas
# -------------------------------

response_schemas = [

    ResponseSchema(
        name="title",
        description="Title of the programming book"
    ),

    ResponseSchema(
        name="author",
        description="Author of the book"
    ),

    ResponseSchema(
        name="difficulty",
        description="Difficulty level of the book"
    ),

    ResponseSchema(
        name="chapters",
        description="A list of chapter names"
    )

]

# -------------------------------
# Create the Parser
# -------------------------------

parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)

# -------------------------------
# Create Prompt
# -------------------------------

prompt = PromptTemplate(
    template="""
Generate a programming book.

Topic:
{topic}

{format_instructions}
""",

    input_variables=["topic"],

    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# -------------------------------
# Load LLM
# -------------------------------

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------------
# Create LCEL Chain
# -------------------------------

chain = prompt | model | parser

# -------------------------------
# Invoke
# -------------------------------

result = chain.invoke({

    "topic": "Python"

})

# -------------------------------
# Output
# -------------------------------

print(result)

print()

print("Title:", result["title"])
print("Author:", result["author"])
print("Difficulty:", result["difficulty"])
print("Chapters:", result["chapters"])