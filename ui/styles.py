"""UI styling configuration."""

CUSTOM_CSS = """
.gradio-container {
    max-width: 1200px;
    margin: auto;
    font-family: 'Segoe UI', sans-serif !important;
}

.chatbot {
    border: 2px solid #6b46c1 !important;
    border-radius: 12px !important;
}

.btn-primary {
    background: linear-gradient(135deg, #8b5cf6, #a855f7) !important;
    border: 2px solid #8b5cf6 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

.status-message {
    background-color: #faf5ff !important;
    border: 1px solid #a855f7 !important;
    border-radius: 6px !important;
    padding: 12px !important;
}

.examples {
    background-color: #fdf4ff !important;
    border: 1px solid #d946ef !important;
    border-radius: 6px !important;
    padding: 16px !important;
    margin-top: 16px !important;
}
"""