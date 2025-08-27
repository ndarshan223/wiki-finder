"""Gradio UI interface module."""

import gradio as gr
from typing import Tuple, List
from .styles import CUSTOM_CSS
from config import UIConfig


class ChatInterface:
    """Handles the Gradio chat interface."""
    
    def __init__(self, chatbot_service, config: UIConfig):
        self.chatbot_service = chatbot_service
        self.config = config
    
    def create_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface."""
        with gr.Blocks(title=self.config.title, css=CUSTOM_CSS) as demo:
            self._create_header()
            self._create_status_display()
            chatbot_ui = self._create_chat_interface()
            self._create_input_section(chatbot_ui)
            self._create_examples()
        
        return demo
    
    def _create_header(self):
        """Create the application header."""
        gr.Markdown("# 🔍 SDLC Tools Semantic Search")
        gr.Markdown(
            "Ask questions about SDLC tools like GitLab, Jira, SonarQube, Nexus, CloudBees, and more. "
            "The system will find relevant documentation and procedures using semantic search."
        )
    
    def _create_status_display(self):
        """Create the status display section."""
        record_count = self.chatbot_service.get_record_count()
        status_emoji = "✅" if record_count > 0 else "❌"
        gr.Markdown(
            f"**{status_emoji} Data Status:** {record_count} records loaded from data/ folder",
            elem_classes=["status-message"]
        )
    
    def _create_chat_interface(self) -> gr.Chatbot:
        """Create the main chat interface."""
        return gr.Chatbot(
            label="Search Results",
            height=self.config.chat_height,
            show_label=True,
            container=True
        )
    
    def _create_input_section(self, chatbot_ui: gr.Chatbot):
        """Create the input section with textbox and button."""
        with gr.Row():
            msg = gr.Textbox(
                label="Enter your query",
                placeholder="How to configure GitLab CI/CD pipeline",
                lines=1,
                max_lines=3,
                scale=4,
                interactive=True
            )
            submit_btn = gr.Button(
                "🔍 Search",
                variant="primary",
                scale=1,
                size="lg"
            )
        
        # Connect input handlers
        msg.submit(self._handle_submit, [msg, chatbot_ui], [chatbot_ui, msg])
        submit_btn.click(self._handle_submit, [msg, chatbot_ui], [chatbot_ui, msg])
    
    def _create_examples(self):
        """Create the examples section."""
        gr.Markdown(
            "### 💡 Example Queries:\n"
            "- How to setup GitLab CI/CD pipeline?\n"
            "- Configure SonarQube quality gates\n"
            "- Jira workflow configuration\n"
            "- Nexus repository management\n"
            "- CloudBees security setup",
            elem_classes=["examples"]
        )
    
    def _handle_submit(self, message: str, history: List) -> Tuple[List, str]:
        """Handle user input submission."""
        if message and message.strip():
            response = self.chatbot_service.search(message.strip())
            history.append([message.strip(), response])
        
        return history, ""