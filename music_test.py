from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

for chunk in llm.stream("What is AI?"):
    print(chunk.content, end="", flush=True)