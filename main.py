"""Main application entry point."""

from core.chatbot_service import ChatbotService
from ui.interface import ChatInterface
from config import AppConfig


def main():
    """Initialize and launch the application."""
    print("Starting SDLC Tools Semantic Search Chatbot...")
    
    # Load configuration
    config = AppConfig()
    
    # Initialize core service
    chatbot_service = ChatbotService(config)
    
    # Create UI interface
    chat_interface = ChatInterface(chatbot_service, config.ui)
    demo = chat_interface.create_interface()
    
    # Launch application
    print("Launching Gradio interface...")
    demo.launch(
        server_name=config.ui.server_name,
        server_port=config.ui.server_port,
        share=False,
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    main()