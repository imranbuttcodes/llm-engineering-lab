# run this to start the server: litellm --config config.yaml --port 4000 

from openai import OpenAI

client = OpenAI(
    api_key="anything",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="reasoning",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in one sentence."
        }
    ]
)

print(response.choices[0].message.content)