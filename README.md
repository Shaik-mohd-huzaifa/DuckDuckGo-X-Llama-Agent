![](https://img.shields.io/badge/innovationlab-3D8BD3)

# 🔎 Search + Summarize Agent

### Tech: Python + UAgents + Nebius AI

This agent accepts a search query, fetches the top 5 results from DuckDuckGo, scrapes content (~3000 characters each), and passes the combined text to Nebius LLM for an intelligent, detailed summary. It’s designed to provide concise and insightful answers from multiple web sources.

⸻

## 📊 Diagram

```js
sequenceDiagram
    actor User
    participant SearchAgent as Search + Summarize Agent
    participant DuckDuckGo as DuckDuckGo
    participant Websites as Web Pages
    participant Nebius as Nebius LLM

    User->>SearchAgent: Send SearchQuery (keyword)
    activate SearchAgent

    SearchAgent->>DuckDuckGo: Fetch Top 5 URLs
    DuckDuckGo-->>SearchAgent: Return Links

    loop For Each Link
        SearchAgent->>Websites: Scrape Webpage Content
        Websites-->>SearchAgent: Return HTML Text
    end

    SearchAgent->>Nebius: Send Combined Text
    Nebius-->>SearchAgent: Return Summary

    SearchAgent->>User: SummaryResult (Text)
    deactivate SearchAgent
```


⸻

## 🧪 Example Input


```
SearchQuery(
    keyword="Top AI trends for 2025"
)
```



⸻

## 📬 Example Output

```
SummaryResult(
    summary="The Future of AI: Top Trends for 2025\n\nAI will transform industries with trends like Multimodal AI, Agentic AI, Edge AI, and Explainable AI. It will impact cybersecurity, healthcare, education, finance, and more. Ethics and sustainability will also become core focuses."
)

```


⸻

## 🧪 Usage Example

You can copy-paste this into a new agent to try it:

f
```
rom uagents import Agent, Context, Model

class SearchQuery(Model):
    keyword: str

class SummaryResult(Model):
    summary: str

agent = Agent()

SEARCH_AGENT_ADDRESS = "agent1qwgnmg90044w29puqm0t5pqweya4372uledwcwquzvxe0nvkfeapjd8dfal"

query = SearchQuery(keyword="Top AI trends for 2025")

@agent.on_event("startup")
async def handle_startup(ctx: Context):
    await ctx.send(SEARCH_AGENT_ADDRESS, query)
    ctx.logger.info(f"Sent search query: {query.keyword}")

@agent.on_message(SummaryResult)
async def handle_summary(ctx: Context, sender: str, msg: SummaryResult):
    ctx.logger.info(f"\n🧠 Summary from Search Agent:\n{msg.summary}")

if __name__ == "__main__":
    agent.run()
```


⸻

## 🖥️ Local Agent Setup

Install dependencies:

`pip install uagents openai beautifulsoup4 requests`

To make this agent run locally:

```
agent = Agent(
    name="user",
    endpoint="http://localhost:8000/submit",
)
```

Run it:

```
python agent.py

```


⸻

🌐 Agent Address

`agent1qwgnmg90044w29puqm0t5pqweya4372uledwcwquzvxe0nvkfeapjd8dfal`