"""
Web Search Skill using DuckDuckGo
"""
import logging
from duckduckgo_search import DDGS
from typing import List, Dict

logger = logging.getLogger(__name__)

class WebSearchSkill:
    """Skill for performing web searches"""
    
    def __init__(self):
        self.ddgs = DDGS()
        
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform a web search.
        
        Args:
            query: The search query.
            max_results: Number of results to return.
            
        Returns:
            List of dictionaries containing 'title', 'href', and 'body'.
        """
        try:
            logger.info(f"WebSearchSkill: Searching for '{query}'")
            results = list(self.ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            logger.error(f"WebSearchSkill: Search failed: {e}")
            return []

    def get_tool_definition(self):
        """Return the Gemini tool definition"""
        return {
            "function_declarations": [
                {
                    "name": "web_search",
                    "description": "Search the web for information using DuckDuckGo. Use this for general knowledge, news, or looking up facts.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query."
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
