"""
FastAPI Chat API - Web interface for Panversity Student Assistant
Serves the modern chatbot UI and handles chat requests
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import json
from datetime import datetime
from pathlib import Path

from src.agents.chat_agent import ChatAgent
from src.agents.main_agent import MainAgent


# Initialize FastAPI app
app = FastAPI(
    title="Panversity Student Assistant",
    description="AI-powered assistant for Panversity students",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
public_dir = Path(__file__).parent.parent.parent / "public"
app.mount("/static", StaticFiles(directory=str(public_dir)), name="static")

# Initialize agents
chat_agent = ChatAgent()
main_agent = MainAgent()


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str
    user_id: str = "default"


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    timestamp: str
    status: str


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the main chatbot UI"""
    index_path = public_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Panversity Assistant</title></head>
            <body>
                <h1>Panversity Student Assistant</h1>
                <p>UI is being set up. Please refresh in a moment.</p>
            </body>
        </html>
        """)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Handle chat message and return AI response
    
    Args:
        message: ChatMessage with user message and user_id
        
    Returns:
        ChatResponse with AI response
    """
    try:
        result = chat_agent.chat(message.message, message.user_id)
        
        # Log to chat history
        await log_to_chat_history({
            "timestamp": result["timestamp"],
            "task": "chat",
            "agent": "ChatAgent",
            "action": "user_message",
            "status": result["status"],
            "data": {
                "user_id": message.user_id,
                "message": message.message,
                "response": result["response"],
                "tokens_used": result.get("tokens_used", 0)
            }
        })
        
        return ChatResponse(
            response=result["response"],
            timestamp=result["timestamp"],
            status=result["status"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat streaming
    
    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            user_id = message_data.get("user_id", "default")
            
            # Send typing indicator
            await websocket.send_json({
                "type": "typing",
                "status": "started"
            })
            
            # Stream response
            full_response = ""
            async for chunk in async_stream_chat(user_message, user_id):
                full_response += chunk
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk
                })
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "timestamp": datetime.now().isoformat()
            })
            
            # Log to chat history
            await log_to_chat_history({
                "timestamp": datetime.now().isoformat(),
                "task": "chat_stream",
                "agent": "ChatAgent",
                "action": "user_message",
                "status": "success",
                "data": {
                    "user_id": user_id,
                    "message": user_message,
                    "response": full_response
                }
            })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })


async def async_stream_chat(user_message: str, user_id: str):
    """Async wrapper for streaming chat"""
    for chunk in chat_agent.stream_chat(user_message, user_id):
        yield chunk


@app.get("/api/status")
async def get_status():
    """Get status of all agents"""
    return {
        "chat_agent": chat_agent.get_status(),
        "main_agent": main_agent.get_status(),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/clear-history")
async def clear_history():
    """Clear chat conversation history"""
    chat_agent.clear_history()
    return {"status": "success", "message": "Chat history cleared"}


@app.get("/api/conversation")
async def get_conversation():
    """Get current conversation history"""
    return {
        "conversation": chat_agent.get_conversation_history(),
        "length": len(chat_agent.get_conversation_history())
    }


async def log_to_chat_history(entry: Dict):
    """Log entry to chat_history"""
    try:
        # Use MainAgent's logging method
        main_agent._log_to_chat_history(
            task=entry["task"],
            data=entry["data"]
        )
    except Exception as e:
        print(f"Error logging to chat history: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
