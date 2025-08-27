import gradio as gr
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

class SemanticSearchChatbot:
    def __init__(self):
        # Try to load local model first, fallback to download
        model_path = './models/all-MiniLM-L6-v2'
        if os.path.exists(model_path):
            self.model = SentenceTransformer(model_path)
        else:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = None
        self.embeddings = None
        
    def load_excel_data(self, file_path):
        """Load data from Excel file with columns: Tool, Action, Summary, Link"""
        try:
            self.data = pd.read_excel(file_path)
            # Create searchable text by combining relevant columns
            self.data['searchable_text'] = (
                self.data['Tool'].astype(str) + ' ' + 
                self.data['Action'].astype(str) + ' ' + 
                self.data['Summary'].astype(str)
            )
            # Generate embeddings
            self.embeddings = self.model.encode(self.data['searchable_text'].tolist())
            return f"Loaded {len(self.data)} records successfully"
        except Exception as e:
            return f"Error loading data: {str(e)}"
    
    def search(self, query, top_k=5):
        """Perform semantic search"""
        if self.data is None or self.embeddings is None:
            return "No data loaded. Please load Excel file first."
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                result = {
                    'tool': self.data.iloc[idx]['Tool'],
                    'action': self.data.iloc[idx]['Action'],
                    'summary': self.data.iloc[idx]['Summary'],
                    'link': self.data.iloc[idx]['Confluence Link'],
                    'similarity': similarities[idx]
                }
                results.append(result)
        
        return self.format_results(results)
    
    def format_results(self, results):
        """Format search results for display"""
        if not results:
            return "No relevant results found."
        
        formatted = "**Search Results:**\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"**{i}. {result['tool']} - {result['action']}**\n"
            formatted += f"Summary: {result['summary']}\n"
            formatted += f"Link: {result['link']}\n"
            formatted += f"Relevance: {result['similarity']:.2f}\n\n"
        
        return formatted

# Initialize chatbot
chatbot = SemanticSearchChatbot()

def chat_interface(message, history):
    """Gradio chat interface"""
    response = chatbot.search(message)
    history.append([message, response])
    return history, ""

def load_data_interface(file):
    """Interface to load Excel data"""
    if file is None:
        return "Please select a file"
    
    result = chatbot.load_excel_data(file.name)
    return result

# Create Gradio interface
with gr.Blocks(title="Semantic Search Chatbot") as demo:
    gr.Markdown("# SDLC Tools Semantic Search Chatbot")
    
    with gr.Tab("Chat"):
        chatbot_ui = gr.Chatbot(label="Search Results")
        msg = gr.Textbox(label="Enter your query", placeholder="e.g., How to configure GitLab CI/CD?")
        msg.submit(chat_interface, [msg, chatbot_ui], [chatbot_ui, msg])
    
    with gr.Tab("Data Management"):
        file_upload = gr.File(label="Upload Excel File", file_types=[".xlsx", ".xls"])
        upload_btn = gr.Button("Load Data")
        status = gr.Textbox(label="Status", interactive=False)
        
        upload_btn.click(load_data_interface, inputs=file_upload, outputs=status)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)