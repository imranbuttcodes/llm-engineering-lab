from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel, RunnableLambda
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


def countLen(text):
    return len(text.split())


# """
# RunnableLambda() EXAMPLE
# def countLen(text):
#     return len(text.split())


# lambda_run = RunnableLambda(countLen)


# print("TEXT LEN:",lambda_run.invoke("Hi, Bro I'm Imran butt , do you know me?"))

# OUTPUT: TEXT LEN: 10 

# """


parser = StrOutputParser()


joke_chain = RunnableSequence(prompt1, model, parser)

joke_explanation_chain = RunnableSequence(prompt2, model, parser)

parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'joke_explanation': joke_explanation_chain,
    'joke_word_counts': RunnableLambda(countLen)
})


chain = RunnableSequence(joke_chain, parallel_chain)

result = chain.invoke({'topic': 'langChain'})

print('Joke:',result['joke'])
print()
print('Joke Explanation:',result['joke_explanation'])
print()
print('Joke Words Counts:',result['joke_word_counts'])
print()
chain.get_graph().print_ascii()