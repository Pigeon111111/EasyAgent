"""
Main entry point for the Agent Project
"""
import argparse
import threading
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)


def run_api():
    """Run the FastAPI server"""
    from api.main import start_server
    logger.info("Starting FastAPI server...")
    start_server()


def run_ui():
    """Run the Gradio UI"""
    from ui.gradio_app import launch_ui
    logger.info("Starting Gradio UI...")
    launch_ui()


def main():
    parser = argparse.ArgumentParser(description="AI Agent Project")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["all", "api", "ui"],
        default="all",
        help="Run mode: all (both), api (FastAPI only), ui (Gradio only)"
    )

    args = parser.parse_args()

    if args.mode == "all":
        # Run both API and UI
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        run_ui()
    elif args.mode == "api":
        run_api()
    elif args.mode == "ui":
        run_ui()


if __name__ == "__main__":
    main()
