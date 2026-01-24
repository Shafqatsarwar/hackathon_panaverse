"""
ChatAgent - Conversational AI agent for Panversity Student Assistant
Uses Google Gemini for natural language understanding with web search capabilities
Integrates with gmail_monitoring, email_filtering, and email_notifications skills
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from duckduckgo_search import DDGS
from src.utils.config import Config
from skills.chatbot_skill.skill import ChatbotSkill


class ChatAgent:
    """Agent for handling conversational interactions with users using Gemini"""
    
    def __init__(self):
        """Initialize ChatAgent with Chatbot Skill"""
        # Initialize Chatbot Skill
        self.chatbot_skill = ChatbotSkill(
            api_key=Config.GOOGLE_API_KEY,
            model_name='gemini-2.5-flash',
            fallback_models=['gemini-2.0-flash']
        )
        
        self.chat_session = None
        self.conversation_history: List[Dict[str, str]] = []
        # System prompt is now handled by the skill context or prepended to history/message if API supports it,
        # but for simplicity we'll keep the system prompt logic or pass it if the skill supported it.
        # The current simple skill doesn't strictly enforce system prompt in __init__, so we'll rely on it behaving as a chat model.
        
    def _build_system_prompt(self) -> str:
        """Build system prompt with agent context and capabilities"""
        return f"""You are the Panversity Student Assistant, an AI-powered helper for students.

Your capabilities and skills:

1. **Email Monitoring** (gmail_monitoring skill):
   - Monitor Gmail inbox for important emails
   - Filter emails by keywords: {', '.join(Config.FILTER_KEYWORDS)}
   - Detect priority levels and deadlines
   
2. **Email Filtering** (email_filtering skill):
   - Categorize emails by type (quiz, assignment, exam, general)
   - Detect priority (High/Medium/Low)
   - Identify deadlines and due dates
   
3. **Email Notifications** (email_notifications skill):
   - Send email alerts to: {Config.ADMIN_EMAIL}
   - Format notifications with priority badges
   - Deliver important updates via SMTP

4. **Web Search**:
   - Search the web for current information
   - Answer questions about topics not in your training data
   - Provide up-to-date information

Current configuration:
- Email monitoring: Active (checks every {Config.EMAIL_CHECK_INTERVAL} minutes)
- Admin contact: {Config.ADMIN_EMAIL}
- WhatsApp: {"Enabled" if Config.WHATSAPP_ENABLED else "Disabled"}
- LinkedIn: {"Enabled" if Config.LINKEDIN_ENABLED else "Disabled"}

When users ask about:
- Emails: Explain how the email monitoring system works
- Tasks/Deadlines: Help them organize and prioritize
- Panversity/PIAIC: Provide information and guidance
- Current events/facts: Use web search to get accurate information

Be helpful, concise, and professional. Use emojis sparingly to make responses friendly."""
    
    def _web_search(self, query: str, max_results: int = 3) -> str:
        """
        Perform web search using DuckDuckGo
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results as string
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
            if not results:
                return "No search results found."
            
            formatted_results = f"Web search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. **{result['title']}**\n"
                formatted_results += f"   {result['body']}\n"
                formatted_results += f"   Source: {result['href']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Web search error: {str(e)}"
    
    def chat(self, user_message: str, user_id: str = "default") -> Dict[str, any]:
        """
        Process a chat message and return Gemini response
        
        Args:
            user_message: The user's message
            user_id: User identifier for context
            
        Returns:
            Dict with response, status, and metadata
        """
        try:
            # Inject Odoo Context if relevant
            odoo_context = ""
            if any(kw in user_message.lower() for kw in ["odoo", "lead", "crm", "sales", "opportunity"]):
                try:
                    from src.agents.odoo_agent import OdooAgent
                    odoo = OdooAgent()
                    if odoo.enabled:
                        summary = odoo.get_recent_leads_summary()
                        odoo_context = f"\n[SYSTEM CONTEXT]\n{summary}\n[END CONTEXT]\n"
                except Exception as e:
                    print(f"ChatAgent: Failed to fetch Odoo context: {e}")

            # Check if web search is needed
            search_keywords = ["search", "find", "look up", "what is", "who is", "current", "latest", "today"]
            needs_search = any(keyword in user_message.lower() for keyword in search_keywords)
            
            # Perform web search if needed
            search_context = ""
            if needs_search:
                # Extract search query (simple heuristic)
                search_query = user_message
                search_context = f"\n\n[Web Search Results]\n{self._web_search(search_query)}"
            
            # Initialize chat session if not exists
            if self.chat_session is None:
                # Prepend system prompt to first message if needed, or strictly use history.
                # For now using the skill's start_chat
                self.chat_session = self.chatbot_skill.start_chat(history=[])
                # Ideally send system prompt as first message if model supports context,
                # or just rely on the model.
                # Let's send the system prompt contextually if it's new session? 
                # Simplification: We'll append the system prompt text to the first user message if needed 
                # or just use the system prompt builder for context.
                
            # Prepare message with search context and system prompt context
            # (Note: Re-adding system prompt to every message is expensive/wrong, 
            # ideally the Agent or Skill handles system instructions better.
            # For this refactor, we keep it simple).
            full_context = ""
            if len(self.conversation_history) == 0:
                 full_context = self._build_system_prompt() + "\n\n"

            full_message = full_context + user_message + search_context
            
            # Get response from Skill
            ai_message = self.chatbot_skill.generate_response(self.chat_session, full_message)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "status": "success",
                "response": ai_message,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "web_search_used": needs_search
            }
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            return {
                "status": "error",
                "response": error_message,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "error": str(e)
            }
    
    def stream_chat(self, user_message: str, user_id: str = "default"):
        """
        Stream chat response for real-time display
        
        Args:
            user_message: The user's message
            user_id: User identifier for context
            
        Yields:
            Chunks of the AI response
        """
        try:
            # Check if web search is needed
            search_keywords = ["search", "find", "look up", "what is", "who is", "current", "latest", "today"]
            needs_search = any(keyword in user_message.lower() for keyword in search_keywords)
            
            # Perform web search if needed
            search_context = ""
            if needs_search:
                search_query = user_message
                search_results = self._web_search(search_query)
                search_context = f"\n\n[Web Search Results]\n{search_results}"
                # Yield search indicator
                yield f"🔍 *Searching the web...*\n\n"
            
            # Initialize chat session if not exists
            if self.chat_session is None:
                self.chat_session = self.chatbot_skill.start_chat(history=[])
            
            # Prepare message with search context
            full_context = ""
            if len(self.conversation_history) == 0:
                 full_context = self._build_system_prompt() + "\n\n"

            full_message = full_context + user_message + search_context
            
            # Stream response from Skill
            full_response = ""
            for chunk in self.chatbot_skill.stream_response(self.chat_session, full_message):
                full_response += chunk
                yield chunk
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history and reset chat session"""
        self.conversation_history = []
        self.chat_session = None
    
    def get_status(self) -> Dict[str, any]:
        """
        Get agent status for observability
        
        Returns:
            Dict with agent status and metrics
        """
        return {
            "agent": "ChatAgent",
            "status": "active",
            "conversation_length": len(self.conversation_history),
            "gemini_configured": bool(Config.GOOGLE_API_KEY),
            "model": "gemini-2.0-flash-exp",
            "skills_available": [
                "gmail_monitoring",
                "email_filtering", 
                "email_notifications",
                "web_search"
            ],
            "web_search": "enabled"
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history.copy()

