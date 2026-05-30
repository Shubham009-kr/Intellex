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

@tool
def scrape_url(url: str) -> str:
    """Scrape the content of the provided url for deeper reading and return the clean text content."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]  # Return first 2000 chars for brevity
    except Exception as e:
        return f"Error scraping URL: {str(e)}"


# print(web_search.invoke("What is the current stock price of Apple Inc.?"))
print(len(scrape_url.invoke("https://www.apple.com/investor/")))