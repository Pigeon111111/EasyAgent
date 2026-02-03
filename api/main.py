"""
FastAPI Backend for Agent Project
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from loguru import logger

from config.settings import API_HOST, API_PORT
from agents.agent import create_simple_agent, run_agent
from loguru import logger

app = FastAPI(
    title="Agent API",
    description="LangChain Agent API with FastAPI",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    system_prompt: Optional[str] = "You are a helpful AI assistant."


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


# In-memory storage for conversations (replace with database in production)
conversations = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Agent API is running"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for agent interaction
    """
    conversation_id = str(uuid.uuid4())

    logger.info(f"Received message: {request.message}")

    # Convert history to the format expected by the agent
    chat_history = [{"role": m.role, "content": m.content} for m in (request.history or [])]

    # Run the agent
    try:
        agent = create_simple_agent()
        if agent is None:
            response_text = "Error: No LLM configured. Please set your API key in .env"
        else:
            response_text = run_agent(agent, request.message, chat_history)
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        response_text = f"Error: {str(e)}"

    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id
    )


@app.get("/api/models")
async def list_models():
    """
    List available LLM models
    """
    return {
        "models": [
            {"id": "gpt-3.5-turbo", "name": "OpenAI GPT-3.5 Turbo"},
            {"id": "gpt-4", "name": "OpenAI GPT-4"},
            {"id": "claude-3-haiku", "name": "Anthropic Claude 3 Haiku"},
            {"id": "claude-3-sonnet", "name": "Anthropic Claude 3 Sonnet"},
        ]
    }


def start_server():
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    start_server()
