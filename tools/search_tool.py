import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

import requests
from crewai.tools import BaseTool

from config.settings import settings


class SearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Search the web for information on a given topic, Input should be a search query string."

    def _run(self, query: str) -> str:
        """Run a web search using Serper API."""
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {"q": query, "num": 5}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("organic", [])[:5]:
                results.append(
                    f"""
                    Title: {item.get('title', '')}
                    Link: {item.get('link', '')}
                    Snippet: {item.get('snippet', '')}
                """
                )

            return "\n---\n".join(results) if results else "No results found."

        except Exception as e:
            return f"Search failed: {str(e)}"


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = input("Enter search query: ").strip()

    if not query:
        print("No query provided.")
        return

    result = SearchTool().run(query)
    print(result)


if __name__ == "__main__":
    main()
