from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import streamlit as st



llm = HuggingFacePipeline.from_model_id(
    model_id = 'HuggingFaceTB/SmolLM2-360M-Instruct',
    task = 'text-generation',
       pipeline_kwargs={
        'temperature':0.5,
        'max_new_tokens':1000
       }
)

model = ChatHuggingFace(llm=llm)


st.header('Yoah Ask Anything')
user_input = st.text_input("Ask Anything", placeholder='Enter your prompt')
if st.button('Send'):
    with st.spinner('Generating...'):
 # Chain the model with a String Output Parser to easily extract raw text
        chain = model | StrOutputParser()
        result = chain.invoke(user_input)
        # Display the output
        st.write(result)
