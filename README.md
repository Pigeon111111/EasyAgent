# AI Agent Project

A modern AI Agent application built with **FastAPI**, **LangChain**, and **Gradio**.

## Features

- 🤖 AI Agent powered by LangChain
- 🌐 FastAPI backend REST API
- 🎨 Beautiful Gradio chat interface
- 🔧 Support for multiple LLM providers (OpenAI, Anthropic, Google)
- 🔍 Web search capability

## Prerequisites

- Python 3.10+
- Conda or virtual environment
- API keys for LLM providers (OpenAI, Anthropic, Google, or **LongCat**)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AgentProject
```

2. Create and activate environment:
```bash
conda create -n agent_env python=3.10
conda activate agent_env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application:
```bash
# Run both API and UI
python main.py

# Or run separately
python main.py --mode api    # FastAPI server on port 8000
python main.py --mode ui     # Gradio UI on port 7860
```

## Project Structure

```
AgentProject/
├── api/                # FastAPI backend
│   └── main.py         # API endpoints
├── agents/             # LangChain agent
│   └── agent.py        # Agent implementation
├── ui/                 # Gradio frontend
│   └── gradio_app.py   # Chat interface
├── config/             # Configuration
│   └── settings.py     # Settings management
├── tests/              # Tests
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── .env.example        # Environment template
```

## API Endpoints

- `GET /` - Health check
- `POST /api/chat` - Chat with the agent
- `GET /api/models` - List available models

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes* |
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes* |
| `GOOGLE_API_KEY` | Google API key | Yes* |
| `LLM_PROVIDER` | LLM provider (openai/antropic/google) | No |
| `LLM_MODEL` | Model name | No |

*At least one API key is required.

## License

Unlicensed - Public Domain. Feel free to use, modify, and distribute freely.
