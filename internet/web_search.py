from duckduckgo_search import DDGS

class WebSearch:
    @staticmethod
    def search(query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "No results found."
                
                output = f"Search results for '{query}':\n"
                for i, res in enumerate(results):
                    output += f"\n[{i+1}] {res['title']}\n{res['body']}\n(Source: {res['href']})\n"
                return output
        except Exception as e:
            return f"Error searching the web: {str(e)}"