from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for a recent and reliable information on the given query. Return Titles, URLs and snippets."""
    results = tavily.search(query=query, max_results=5)

    out  = []
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n------\n".join(out)



print(web_search.invoke("What is the current stock price of Apple Inc.?"))