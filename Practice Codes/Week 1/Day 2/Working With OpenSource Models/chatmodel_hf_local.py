from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv
import os

os.environ['HF_HOME'] = 'D:/huggingface_cache'


llm = HuggingFacePipeline.from_model_id(
    model_id = 'HuggingFaceTB/SmolLM2-360M-Instruct',
    task = 'text-generation',
       pipeline_kwargs={
        'temperature':0.5,
        'max_new_tokens':100
       }
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("What is 5 * 39 , also explain what is AI?")

print(result.content)
# from transformers import pipeline

# pipe = pipeline(
#     "text-generation",
#     model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# )

# result = pipe(
#     "What is 5 * 3?",
#     max_new_tokens=50
# )

# print(result[0]["generated_text"])