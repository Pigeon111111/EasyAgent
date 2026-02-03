"""
Gradio UI for Agent Chat using AgentChatUI
"""
from ui.agentchatui import AgentChatUI
from config.settings import API_PORT, GRADIO_PORT


def create_gradio_interface():
    """
    Create the Gradio chat interface using AgentChatUI
    """
    ui = AgentChatUI(
        api_url=f"http://localhost:{API_PORT}/api/chat",
        title="🤖 AI Agent Chat"
    )
    return ui.create_interface()


def launch_ui():
    """
    Launch the Gradio UI
    """
    from ui.agentchatui import AgentChatUI
    ui = AgentChatUI(
        api_url=f"http://localhost:{API_PORT}/api/chat",
        title="🤖 AI Agent Chat"
    )
    ui.launch(server_port=GRADIO_PORT, share=False)


if __name__ == "__main__":
    launch_ui()
