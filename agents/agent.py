"""
LangChain Agent Implementation
Compatible with LangChain 1.2.8
"""
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import (
    LLM_PROVIDER, LLM_MODEL, AGENT_MODEL_TEMPERATURE,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, LONGCAT_API_BASE, LONGCAT_API_KEY
)
from loguru import logger


def get_llm():
    """
    Get the configured LLM based on settings
    """
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        logger.info(f"Using OpenAI model: {LLM_MODEL}")
        return ChatOpenAI(
            model=LLM_MODEL,
            temperature=AGENT_MODEL_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
    elif LLM_PROVIDER == "longcat" and LONGCAT_API_BASE:
        logger.info(f"Using LongCat model: {LLM_MODEL}")
        return ChatOpenAI(
            model=LLM_MODEL,
            temperature=AGENT_MODEL_TEMPERATURE,
            api_key=LONGCAT_API_KEY or OPENAI_API_KEY,
            model_kwargs={"base_url": LONGCAT_API_BASE}
        )
    elif LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        logger.info(f"Using Anthropic model: {LLM_MODEL}")
        return ChatAnthropic(
            model=LLM_MODEL,
            temperature=AGENT_MODEL_TEMPERATURE,
            api_key=ANTHROPIC_API_KEY
        )
    else:
        logger.warning("No valid API key found")
        return None


def create_simple_agent():
    """
    Create a simple LLM-based agent (without complex tool use)
    For full agent functionality, upgrade to LangChain 0.3+
    """
    llm = get_llm()
    if llm is None:
        return None

    # Simple chain without tools
    prompt = PromptTemplate.from_template("""You are a helpful AI assistant.

Current conversation:
{chat_history}

Human: {input}

Assistant:""")

    chain = prompt | llm | StrOutputParser()

    return chain


def run_agent(chain, message: str, chat_history: list = None):
    """
    Run the agent with a message and return the response
    """
    if chain is None:
        return "Error: No LLM configured. Please set your API key in .env"

    if chat_history is None:
        chat_history = []

    # Format chat history
    formatted_history = ""
    for msg in chat_history:
        if msg.get("role") == "human":
            formatted_history += f"Human: {msg.get('content', '')}\n"
        else:
            formatted_history += f"Assistant: {msg.get('content', '')}\n"

    try:
        response = chain.invoke({
            "input": message,
            "chat_history": formatted_history
        })
        return response.strip()
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        return f"Error: {str(e)}"


def create_agent_with_search():
    """
    Create an agent with web search capability
    """
    llm = get_llm()
    if llm is None:
        return None

    # Search tool
    search = DuckDuckGoSearchRun()

    # Create a prompt that includes search capability
    prompt = PromptTemplate.from_template("""You are a helpful AI assistant with web search capability.

If you need to find current information, use the search tool.

Current conversation:
{chat_history}

Human: {input}

Assistant:""")

    chain = prompt | llm | StrOutputParser()

    return chain, search
