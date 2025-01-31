from dotenv import load_dotenv
from duckduckgo_search import DDGS
import feedparser

load_dotenv()

async def search_itmo_news(query: str) -> list:
    """Ищет информацию по Университету ИТМО через DuckDuckGo."""
    with DDGS() as ddgs:
        results = ddgs.text(f"{query} site:itmo.ru", max_results=3)
    return [result["href"] for result in results]

def get_itmo_rss_news() -> list:
    """Парсит последние новости из RSS ITMO News."""
    url = "https://news.itmo.ru/ru/rss/"
    feed = feedparser.parse(url)
    return [entry["link"] for entry in feed.entries[:3]]