from fastmcp import FastMCP
import random
import requests
import os
mcp = FastMCP(name = 'demo-server')

@mcp.tool
def add(a: int, b: int) -> int:
    """
    this function returns summition of two numbers
    """

    return a + b

@mcp.tool
def roll_dice(n_dic: int = 1) -> list[int]:
    """
    rolls n_dice 6-sided dice and return the results.
    """
    return [random.randint(1, 6) for _ in range(n_dic)]

@mcp.tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()



if __name__ == '__main__':
    mcp.run()