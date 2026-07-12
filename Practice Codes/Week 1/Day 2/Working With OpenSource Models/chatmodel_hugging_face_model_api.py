from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="OpenMOSS-Team/MOSS-Transcribe-Diarize",
    task = "text-generation",
        huggingfacehub_api_token=api_key
)

model = ChatHuggingFace(llm=llm)

response = model.invoke('Hi bro!')
print(response.content)
