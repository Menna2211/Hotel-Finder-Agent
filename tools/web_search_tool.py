from langchain_core.tools import tool
import requests

@tool
def web_search(query: str) -> str:
    """Perform a web search using the Tavily API to retrieve hotel info."""
    API_KEY = "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"

    response = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"query": query}
    )

    if response.status_code != 200:
        return f"Search API error: {response.status_code}"

    data = response.json()
    if not data.get("results"):
        return "No search results found."

    top_results = "\n\n".join([
        f"🏨 {r['title']}\n{r['content']}\n🔗 {r['url']}"
        for r in data["results"][:5]
    ])
    return top_results
