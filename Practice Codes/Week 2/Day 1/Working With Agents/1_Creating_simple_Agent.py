from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import Client
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
import os

load_dotenv()


search_tool = DuckDuckGoSearchRun()


EXCHANGE_API_KEY = os.getenv('CURRENCY_RATE_API_KEY')

@tool
def get_conversion_rate(
    base_currency: str,
    target_currency: str,
) -> float:
    """
     Fetches the currency exchange rate.
    Get exchange rate.

    ALWAYS call this tool using JSON.

    Example:

    {
      "base_currency":"USD",
      "target_currency":"INR"
    }
    Args:
        base_currency: The starting currency code (e.g., 'USD'). Do NOT combine multiple currencies here.
        target_currency: The destination currency code (e.g., 'PKR').
    """

    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{EXCHANGE_API_KEY}/pair/"
        f"{base_currency}/{target_currency}"
    )

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    return data["conversion_rate"]


@tool
def convert_currency(
    amount: float,
    conversion_rate: float,
) -> float:
    """
    Converts an amount using a conversion rate.
    """

    return amount * conversion_rate


client = Client()
prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)
print(prompt)


llm = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    api_key = os.getenv("GROQ_API_KEY")
)


agent = create_react_agent(
    llm=llm,
    tools=[convert_currency, get_conversion_rate, search_tool],
    prompt=prompt
)


agent_executer = AgentExecutor(
    agent=agent,
    tools=[convert_currency, get_conversion_rate, search_tool],
    verbose=True # so that agent can print its thinking/reasoning and action stuff.
)


while True:
    query = input("Ask Anythin: ")
    if query == 'break':
        break
    response = agent_executer.invoke({
        'input': query
    }    
    )


    #print(response)

    print(response['output'])