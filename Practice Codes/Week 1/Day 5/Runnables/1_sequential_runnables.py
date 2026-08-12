from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))



prompt1 = PromptTemplate(
    template = 'Generate a one line joke on topic {topic}',
    input_variables= ['topic']
)


prompt2 = PromptTemplate(
    template = 'Explain the Joke in a Saddest Way {joke}',
    input_variables=['joke']
)

parser = StrOutputParser()


chain = RunnableSequence(prompt1, model, parser, model, parser)

result = chain.invoke({'topic': 'AI'})

print(result)

# Now what if we also wanna see that what was the joke itself?
# So for this kinda scenerios we ues RunnablePassThrough() 