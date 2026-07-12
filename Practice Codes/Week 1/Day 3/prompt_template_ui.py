from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, load_prompt
from langchain_groq import ChatGroq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    groq_api_key = api_key
)

#model = ChatHuggingFace(llm=llm)


# Create the template
# prompt = PromptTemplate.from_template("""
# You are an experienced Computer Science teacher.

# Answer the following user request.

# User Request:
# {question}

# Difficulty:
# {level}

# Guidelines:
# - Start with the sentence Hi CS DUDE
# - Explain clearly.
# - Use simple language.
# - Give one real-life analogy.
# - Include one Python example Only if relevant or user talking about Codes, not for just greetings although you can generate code if you think is relevent.
# - Keep the answer well structured.
# - Also use Emojis (Not too much) in structured way as CHATGPT DOes
# """
# )



prompt = load_prompt('prompt_template.json')

# print(final_prompt.text)

st.header('AI Learning Assistant')
question = st.text_input("Ask Anything", placeholder='Enter your prompt')
level = st.selectbox(
    "Difficulty",
    [
        "5-Year-Old",
        "Beginner",
        "Intermediate",
        "Advanced",
        "Professional"
    ]
)
if st.button('Send'):
    with st.spinner('Generating...'):
 # Fill the placeholders
        final_prompt = prompt.invoke({
            "question": question,
            "level": level
        })

        result = model.invoke(final_prompt)
        # Display the output
        st.write(result.content)
