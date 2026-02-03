"""
AgentChatUI - A simple chat UI wrapper for AI Agents
Compatible with LangChain and other agent frameworks
"""
import gradio as gr
import httpx
from typing import Callable, Optional, List, Dict, Any


class AgentChatUI:
    """
    A simple and beautiful chat UI for AI Agents
    """

    def __init__(
        self,
        api_url: str = "http://localhost:8000/api/chat",
        title: str = "🤖 AI Agent Chat",
        theme: Optional[str] = "soft"
    ):
        self.api_url = api_url
        self.title = title
        self.theme = theme
        self.history = []

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface"""

        with gr.Blocks(title=self.title, theme=gr.themes.Soft()) as demo:
            gr.Markdown(f"# {self.title}")

            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        height=500,
                        bubble_full_width=False,
                        avatar_images=(None, "https://i.imgur.com/4y4K8rM.png")
                    )

                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        scale=5,
                        show_label=False
                    )

                    with gr.Row():
                        clear_btn = gr.Button("Clear", variant="secondary")
                        send_btn = gr.Button("Send", variant="primary")

                with gr.Column(scale=1):
                    gr.Markdown("### Settings")
                    system_prompt = gr.Textbox(
                        value="You are a helpful AI assistant.",
                        label="System Prompt",
                        lines=3
                    )

            # Event handlers
            def respond(message, history, system_prompt):
                if not message.strip():
                    return "", history

                history.append((message, None))

                try:
                    client = httpx.Client()
                    response = client.post(
                        self.api_url,
                        json={
                            "message": message,
                            "history": [{"role": "human", "content": h[0]} for h in history[:-1]],
                            "system_prompt": system_prompt
                        },
                        timeout=30.0
                    )

                    if response.status_code == 200:
                        data = response.json()
                        bot_response = data.get("response", "I couldn't get a response.")
                    else:
                        bot_response = f"Error: {response.status_code}"

                    client.close()

                except Exception as e:
                    bot_response = f"Sorry, I encountered an error: {str(e)}"

                history[-1] = (message, bot_response)
                return "", history

            def clear_chat():
                return [], ""

            send_btn.click(
                fn=respond,
                inputs=[msg, chatbot, system_prompt],
                outputs=[msg, chatbot]
            )

            msg.submit(
                fn=respond,
                inputs=[msg, chatbot, system_prompt],
                outputs=[msg, chatbot]
            )

            clear_btn.click(fn=clear_chat, outputs=[chatbot, msg])

        return demo

    def launch(self, server_port: int = 7860, share: bool = False):
        """Launch the UI"""
        demo = self.create_interface()
        demo.launch(server_port=server_port, share=share)


def create_chat_ui(api_url: str = "http://localhost:8000/api/chat") -> gr.Blocks:
    """Factory function to create chat UI"""
    ui = AgentChatUI(api_url=api_url)
    return ui.create_interface()


if __name__ == "__main__":
    # Demo launch
    ui = AgentChatUI()
    ui.launch(server_port=7860)
