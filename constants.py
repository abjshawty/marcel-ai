# Imports
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
import os

load_dotenv()
# Constants
PDF_FOLDER = "/pdf"
RECURSIVE_CHARACTER_TEXT_SPLITTER_CHUNK_SIZE = 500
RECURSIVE_CHARACTER_TEXT_SPLITTER_CHUNK_OVERLAP = 100
MILVUS_IP = os.getenv("MILVUS_IP")
MILVUS_PORT = os.getenv("MILVUS_PORT")
MILVUS_URI = f"http://{MILVUS_IP}:{MILVUS_PORT}"

# Messages
EMBED_FOLDER_FAILURE = "Failed to embed folder."
EMBED_FOLDER_SUCCESS = "Folder embedded successfully."
EMBED_FILE_FAILURE = "Failed to embed file."
EMBED_FILE_SUCCESS = "File embedded successfully."
EMBED_QUERY_FAILURE = "Failed to embed query."
EMBED_QUERY_SUCCESS = "Query embedded successfully."
VECTOR_SEARCH_FAILURE = "Failed to search vector."
VECTOR_SEARCH_SUCCESS = "Vector searched successfully."

# Classes
class Success:
    success: bool
    message: str
    def __init__(self, message: str = "Success"):
        self.success = True
        self.message = message

class Failure:
    success: bool
    message: str
    def __init__(self, error: Exception):
        self.success = False
        self.message = error

# Singletons
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)
