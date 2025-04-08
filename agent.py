import os
import requests
from bs4 import BeautifulSoup
from uagents import Agent, Context, Model
from openai import OpenAI
from urllib.parse import urlparse
from typing import List

# Configure Nebius client
client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

# Message models
class SearchQuery(Model):
    keyword: str

class SummaryResult(Model):
    summary: str

# Create the agent
search_agent = Agent(name="search_agent", port=8001, seed="search agent")

@search_agent.on_event("startup")
async def start(ctx: Context):
    ctx.logger.info("✅ Search Agent is running!")
    ctx.logger.info(f"📬 Agent Address: {search_agent.address}")

@search_agent.on_message(model=SearchQuery)
async def handle_search(ctx: Context, sender: str, query: SearchQuery):
    ctx.logger.info(f"🔍 Searching for: {query.keyword} from {sender}")

    try:
        urls = get_top_5_links(query.keyword)
        scraped_texts = []

        for url in urls:
            ctx.logger.info(f"🌐 Scraping: {url}")
            content = scrape_content(url)
            if content:
                scraped_texts.append(content[:3000])  # limit to 3000 chars each

        combined_text = "\n\n".join(scraped_texts)
        summary = summarize_with_nebius(combined_text)

        ctx.logger.info(f"🧠 Summary: {summary[:300]}...")  # log preview
        await ctx.send(sender, SummaryResult(summary=summary))

    except Exception as e:
        ctx.logger.error(f"❌ Search failed: {e}")


def get_top_5_links(query: str) -> List[str]:
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {"q": query}
    response = requests.post("https://html.duckduckgo.com/html", data=data, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="result__a", limit=5)

    return [a["href"] for a in links if "href" in a.attrs]


def scrape_content(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script/style tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return ""


def summarize_with_nebius(content: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligent assistant. Summarize the information below in a detailed and informative way."
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Nebius summarization failed: {e}"


if __name__ == "__main__":
    print(f"📬 Agent Address: {search_agent.address}")
    search_agent.run()