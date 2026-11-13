import logging
from ddgs import DDGS
from core.tool_result import ToolResult

log = logging.getLogger("EVOX.INTERNET")

class WebSearch:
    @staticmethod
    def search(query: str) -> ToolResult:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return ToolResult.failure("No results found.")
                
                output = f"Search results for '{query}':\n"
                for i, res in enumerate(results):
                    output += f"\n[{i+1}] {res['title']}\n{res['body']}\n(Source: {res['href']})\n"
                return ToolResult.success(output)
        except Exception as e:
            log.error(f"Web-Suche Fehler: {e}")
            return ToolResult.failure(f"Error searching the web: {str(e)}")