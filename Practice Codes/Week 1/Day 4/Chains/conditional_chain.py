from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_groq import ChatGroq 
from pydantic import BaseModel, Field
from typing import Literal


load_dotenv()


model_1 = ChatGroq(model = 'llama-3.3-70b-versatile',
                   groq_api_key = os.getenv("GROQ_API_KEY"))



class Rule(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Classify this Feedback as Positive or Negativee')


parser1 = PydanticOutputParser(pydantic_object=Rule)
parser2 = StrOutputParser()


prompt_1 = PromptTemplate(
    template="""Classify this Feedback as positive or negative
     {format_instructions}
     FeedBack: 
     {feedback}
    """,
    input_variables=['feedback'] ,
    partial_variables={
        'format_instructions': parser1.get_format_instructions()
    }
)


prompt_2 = PromptTemplate(
    template = 'Write an appropriate response to this positive feedback: \n{feedback}',
    input_variables= ['feedback']
)

prompt_3 = PromptTemplate(
    template = 'Write an appropriate response to this negative feedback: \n{feedback}',
    input_variables= ['feedback']
)


classification_chain = prompt_1 | model_1 | parser1


branch_chain = RunnableBranch(
        (lambda x: x.sentiment == 'positive', prompt_2 | model_1 | parser2), # (condition, chain)
        (lambda x: x.sentiment == 'negative', prompt_3 | model_1 | parser2), # (condition, chain)
        RunnableLambda(lambda x: "Couldn't find any Sentiment") # default ,it run if none of them runs above
)


chain = classification_chain | branch_chain | parser2



response = chain.invoke({'feedback': 'This Product is not good at all!'})

print(response)

chain.get_graph().print_ascii()