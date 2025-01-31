import aiohttp
import asyncio
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import feedparser

async def fetch_page_text(url: str, n_abz:int=1) -> str:
    """Асинхронно получает HTML-страницу и извлекает основной текст."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Попытка извлечь самый важный текст (заголовки и абзацы)
                    title = soup.title.string if soup.title else ""
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

                    content = f"{title}\n\n" + "\n".join(paragraphs[:n_abz])
                    return content.strip()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return ""

async def search_itmo_news(query: str) -> list:
    """Ищет информацию по Университету ИТМО и получает краткое содержание страниц."""
    links = []
    with DDGS() as ddgs:
        results = ddgs.text(f"{query} site:itmo.ru", max_results=3)

    for result in results:
        url = result["href"]
        links.append(url)

    # Асинхронно загружаем текст страниц
    page_texts = await asyncio.gather(*(fetch_page_text(url) for url in links))
    # Формируем результат
    return [{"url": url, "summary": summary} for url, summary in zip(links, page_texts)]


def get_itmo_rss_news() -> list:
    """Парсит последние новости из RSS ITMO News."""
    url = "https://news.itmo.ru/ru/rss/"
    feed = feedparser.parse(url)
    return [entry["link"] for entry in feed.entries[:3]]