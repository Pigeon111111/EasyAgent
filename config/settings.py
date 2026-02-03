"""
Configuration for the Agent Project
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# API Keys - GET THESE FROM https://platform.openai.com, https://console.anthropic.com, etc.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY", "")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE", "https://api.longcat.chat/openai")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, google, huggingface, longcat
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# Agent Configuration
AGENT_MODEL_TEMPERATURE = float(os.getenv("AGENT_MODEL_TEMPERATURE", "0.7"))
AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "2000"))

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
GRADIO_PORT = int(os.getenv("GRADIO_PORT", "7860"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
