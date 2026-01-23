"""
ChatAgent - Conversational AI agent for Panversity Student Assistant
Uses Google Gemini for natural language understanding with web search capabilities
Integrates with gmail_monitoring, email_filtering, and email_notifications skills
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import google.generativeai as genai
from duckduckgo_search import DDGS
from src.utils.config import Config


class ChatAgent:
    """Agent for handling conversational interactions with users using Gemini"""
    
    def __init__(self):
        """Initialize ChatAgent with Gemini client"""
        # Configure Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Initialize Gemini model with tools
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            system_instruction=self._build_system_prompt()
        )
        
        self.chat_session = None
        self.conversation_history: List[Dict[str, str]] = []
        
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
                self.chat_session = self.model.start_chat(history=[])
            
            # Prepare message with search context
            full_message = user_message + search_context
            
            # Get response from Gemini
            response = self.chat_session.send_message(full_message)
            ai_message = response.text
            
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
                self.chat_session = self.model.start_chat(history=[])
            
            # Prepare message with search context
            full_message = user_message + search_context
            
            # Stream response from Gemini
            response = self.chat_session.send_message(full_message, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text
            
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

