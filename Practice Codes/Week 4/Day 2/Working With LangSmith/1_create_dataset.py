import os
from dotenv import load_dotenv

from langsmith import Client

load_dotenv()

client = Client(
    api_key=os.getenv("LANGCHAIN_API_KEY")
)

DATASET_NAME = "Nexus Evaluation Dataset (for Learning)"

examples = [
    {
        "inputs": {
            "question": "What is Artificial Intelligence?"
        },
        "outputs": {
            "answer": "Artificial Intelligence is the simulation of human intelligence by machines."
        },
        "metadata": {
            "category": "General"
        }
    },
    {
        "inputs": {
            "question": "Write a Python function to calculate factorial."
        },
        "outputs": {
            "answer": "def factorial(n): ..."
        },
        "metadata": {
            "category": "Coding"
        }
    },
    {
        "inputs": {
            "question": "Explain recursion in simple words."
        },
        "outputs": {
            "answer": "Recursion is when a function calls itself."
        },
        "metadata": {
            "category": "Programming"
        }
    },

    {
        "inputs": {
            "question": "What is the square root of 144?"
        },
        "outputs": {
            "answer": "The square root of 144 is 12."
        },
        "metadata": {
            "category": "Mathematics"
        }
    },
    {
        "inputs": {
            "question": "What is the chemical symbol for gold?"
        },
        "outputs": {
            "answer": "The chemical symbol for gold is Au."
        },
        "metadata": {
            "category": "Science"
        }
    },
    {
        "inputs": {
            "question": "Who was the first President of the United States?"
        },
        "outputs": {
            "answer": "George Washington was the first President of the United States."
        },
        "metadata": {
            "category": "History"
        }
    },
    {
        "inputs": {
            "question": "What is the capital of Japan?"
        },
        "outputs": {
            "answer": "The capital of Japan is Tokyo."
        },
        "metadata": {
            "category": "Geography"
        }
    },
    {
        "inputs": {
            "question": "What does HTML stand for?"
        },
        "outputs": {
            "answer": "HTML stands for HyperText Markup Language."
        },
        "metadata": {
            "category": "Technology"
        }
    }

]

for example in examples:

    client.create_example(
        dataset_name=DATASET_NAME,
        inputs=example["inputs"],
        outputs=example["outputs"],
        metadata=example["metadata"]
    )

print(" Dataset populated successfully.")