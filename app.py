# Core imports for the semantic search chatbot application
import gradio as gr                                    # Web UI framework
import pandas as pd                                    # Data manipulation and analysis
import numpy as np                                     # Numerical computing
from sentence_transformers import SentenceTransformer  # Pre-trained sentence embedding models
from sklearn.metrics.pairwise import cosine_similarity # Similarity calculation
import os                                              # Operating system interface
import glob                                            # File pattern matching

class SemanticSearchChatbot:
    """
    A semantic search chatbot for SDLC tools documentation.
    
    This class handles:
    - Loading and indexing data from Excel/CSV files
    - Converting text to vector embeddings using sentence transformers
    - Performing semantic search using cosine similarity
    - Formatting search results for display
    """
    
    def __init__(self):
        """
        Initialize the chatbot with sentence transformer model and load data.
        
        The model 'all-MiniLM-L6-v2' is lightweight (~80MB) and suitable for
        resource-constrained environments while providing good semantic understanding.
        """
        print("Initializing Semantic Search Chatbot...")
        
        # Try to load local model first (for offline usage), fallback to download
        model_path = './models/all-MiniLM-L6-v2'
        if os.path.exists(model_path):
            print(f"Loading local model from {model_path}")
            self.model = SentenceTransformer(model_path)
        else:
            print("Downloading sentence transformer model (first run only)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize data storage
        self.data = None           # Pandas DataFrame containing the loaded data
        self.embeddings = None     # Numpy array of sentence embeddings
        
        # Load and index all data files from the data folder
        self.load_data_from_folder()
        
    def load_data_from_folder(self):
        """
        Load and index all Excel/CSV files from the data folder.
        
        Expected file format:
        - Tool: Name of the SDLC tool (e.g., GitLab, Jira, SonarQube)
        - Action: Specific action or task (e.g., Setup CI/CD Pipeline)
        - Summary: Detailed description of the action
        - Confluence Link: URL to documentation
        
        The function combines multiple columns into searchable text and
        generates vector embeddings for semantic search.
        """
        print("Loading data files from data/ folder...")
        
        # Find all Excel and CSV files in the data directory
        data_files = glob.glob('data/*.xlsx') + glob.glob('data/*.csv')
        
        if not data_files:
            print("WARNING: No data files found in data/ folder")
            print("Please add Excel (.xlsx) or CSV (.csv) files to the data/ directory")
            return
        
        all_data = []  # List to store DataFrames from all files
        
        # Load each data file
        for file_path in data_files:
            try:
                # Load based on file extension
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
                
                # Validate required columns
                required_columns = ['Tool', 'Action', 'Summary', 'Confluence Link']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    print(f"WARNING: {file_path} missing columns: {missing_columns}")
                    continue
                
                all_data.append(df)
                print(f"✓ Loaded {len(df)} records from {file_path}")
                
            except Exception as e:
                print(f"ERROR loading {file_path}: {str(e)}")
        
        # Combine all data and create embeddings
        if all_data:
            # Concatenate all DataFrames
            self.data = pd.concat(all_data, ignore_index=True)
            
            # Remove any duplicate entries
            initial_count = len(self.data)
            self.data = self.data.drop_duplicates(subset=['Tool', 'Action'], keep='first')
            final_count = len(self.data)
            
            if initial_count != final_count:
                print(f"Removed {initial_count - final_count} duplicate entries")
            
            # Create searchable text by combining relevant columns
            # This creates a single text field for semantic search
            self.data['searchable_text'] = (
                self.data['Tool'].astype(str) + ' ' + 
                self.data['Action'].astype(str) + ' ' + 
                self.data['Summary'].astype(str)
            )
            
            print("Generating embeddings for semantic search...")
            # Convert text to vector embeddings using sentence transformer
            # This is the computationally intensive step
            self.embeddings = self.model.encode(
                self.data['searchable_text'].tolist(),
                show_progress_bar=True
            )
            
            print(f"✓ Successfully indexed {len(self.data)} records for semantic search")
        else:
            print("ERROR: No valid data files could be loaded")
    
    def search(self, query, top_k=5):
        """
        Perform semantic search on the loaded data.
        
        Args:
            query (str): User's search query
            top_k (int): Maximum number of results to return
            
        Returns:
            str: Formatted search results or error message
            
        The search process:
        1. Convert query to vector embedding
        2. Calculate cosine similarity with all data embeddings
        3. Sort by similarity and return top matches
        4. Filter results by minimum similarity threshold
        """
        # Check if data is loaded
        if self.data is None or self.embeddings is None:
            return "❌ No data loaded from data/ folder. Please check data files and restart the application."
        
        if not query or query.strip() == "":
            return "Please enter a search query."
        
        try:
            # Convert user query to vector embedding
            query_embedding = self.model.encode([query.strip()])
            
            # Calculate cosine similarity between query and all data embeddings
            # Cosine similarity ranges from -1 to 1, where 1 is identical
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get indices of top results sorted by similarity (descending)
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            # Filter results by minimum similarity threshold (0.1 = 10% similarity)
            for idx in top_indices:
                if similarities[idx] > 0.1:
                    result = {
                        'tool': self.data.iloc[idx]['Tool'],
                        'action': self.data.iloc[idx]['Action'],
                        'summary': self.data.iloc[idx]['Summary'],
                        'link': self.data.iloc[idx]['Confluence Link'],
                        'similarity': similarities[idx]
                    }
                    results.append(result)
            
            return self.format_results(results, query)
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def format_results(self, results, query=""):
        """
        Format search results for display in the chat interface.
        
        Args:
            results (list): List of search result dictionaries
            query (str): Original search query for context
            
        Returns:
            str: Formatted results in Markdown format
        """
        if not results:
            return f"🔍 No relevant results found for: '{query}'\n\n" + \
                   "💡 **Tips:**\n" + \
                   "- Try different keywords\n" + \
                   "- Use tool names (GitLab, Jira, SonarQube, etc.)\n" + \
                   "- Search for actions (setup, configure, deploy, etc.)"
        
        # Header with result count
        formatted = f"🔍 **Found {len(results)} result(s) for:** '{query}'\n\n"
        
        # Format each result with clear structure
        for i, result in enumerate(results, 1):
            # Similarity percentage for user understanding
            similarity_percent = int(result['similarity'] * 100)
            
            formatted += f"**{i}. {result['tool']} - {result['action']}** ({similarity_percent}% match)\n"
            formatted += f"📝 **Summary:** {result['summary']}\n"
            formatted += f"🔗 **Documentation:** [{result['link']}]({result['link']})\n\n"
        
        return formatted

# Initialize the chatbot instance
# This happens at module level so the model loads once when the app starts
print("Starting application...")
chatbot = SemanticSearchChatbot()

def chat_interface(message, history):
    """
    Handle chat interactions between user and the semantic search system.
    
    Args:
        message (str): User's input message/query
        history (list): Chat history as list of [user_message, bot_response] pairs
        
    Returns:
        tuple: (updated_history, empty_string_to_clear_input)
    """
    # Perform semantic search on user's message
    response = chatbot.search(message)
    
    # Add the interaction to chat history
    history.append([message, response])
    
    # Return updated history and empty string to clear the input box
    return history, ""

# Create the Gradio web interface
with gr.Blocks(
    title="SDLC Tools Semantic Search",
    theme=gr.themes.Soft(),  # Use a clean, professional theme
    css=".gradio-container {max-width: 1200px; margin: auto;}"
) as demo:
    
    # Application header and status
    gr.Markdown("# 🔍 SDLC Tools Semantic Search Chatbot")
    gr.Markdown(
        "Ask questions about SDLC tools like GitLab, Jira, SonarQube, Nexus, CloudBees, and more. "
        "The system will find relevant documentation and procedures using semantic search."
    )
    
    # Display data loading status
    data_count = len(chatbot.data) if chatbot.data is not None else 0
    status_emoji = "✅" if data_count > 0 else "❌"
    gr.Markdown(f"**{status_emoji} Data Status:** {data_count} records loaded from data/ folder")
    
    # Main chat interface
    chatbot_ui = gr.Chatbot(
        label="Search Results",
        height=500,
        show_label=True,
        container=True
    )
    
    # User input textbox
    msg = gr.Textbox(
        label="Enter your query",
        placeholder="e.g., How to configure GitLab CI/CD pipeline? or Setup SonarQube quality gates",
        lines=2,
        max_lines=5
    )
    
    # Connect input submission to chat interface
    msg.submit(chat_interface, [msg, chatbot_ui], [chatbot_ui, msg])
    
    # Add example queries for user guidance
    gr.Markdown(
        "### 💡 Example Queries:\n"
        "- How to setup GitLab CI/CD pipeline?\n"
        "- Configure SonarQube quality gates\n"
        "- Jira workflow configuration\n"
        "- Nexus repository management\n"
        "- CloudBees security setup"
    )

# Application entry point
if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Standard port for Gradio apps
        share=False,            # Set to True for public sharing via gradio.live
        show_error=True,        # Show detailed error messages
        quiet=False             # Show startup logs
    )