from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxxxxxx",
    base_url="https://agentrouter.org/v1",
)

response = client.responses.create(
    model="gpt-5.5",
    input="Hello! Tell me a joke."
)

print(response.output_text)