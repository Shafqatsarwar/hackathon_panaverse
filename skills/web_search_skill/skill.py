"""
Web Search Skill using DuckDuckGo
"""
import logging
# from duckduckgo_search import DDGS (Commented out due to Windows Asyncio Conflict)
from typing import List, Dict

logger = logging.getLogger(__name__)

class WebSearchSkill:
    """Skill for performing web searches"""
    
    def __init__(self):
        # self.ddgs = DDGS() # Lazy init to avoid loop crash
        pass
        
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Perform a web search."""
        try:
            logger.info(f"WebSearchSkill: Searching for '{query}'")
            # Mock return since library is disabled on this env
            return [{"title": "Web Search Unavailable", "body": "Search is currently disabled on this environment due to driver conflicts.", "href": "#"}]
        except Exception as e:
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
