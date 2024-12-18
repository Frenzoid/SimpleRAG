
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from configs import Configs
import shutil
import os

# This class is responsible for managing the database, including initializing, loading, and querying the database.
class DatabaseManager:

    # Constructor
    def __init__(self):
        print(f"Loading embeddings model: {Configs.EMBEDDINGS_MODEL}")
        self.embeddings =  HuggingFaceEmbeddings(model_name=Configs.EMBEDDINGS_MODEL)
        self.database: Chroma

    
    # Initialize the database, either by loading an existing database or creating a new one.
    def initialize_database(self, chunks):

        # If the database already exists, but we dont prelaod, then we delete it.
        if os.path.exists(Configs.CHROMADB_PATH):
            print(f"Deleting old database at {Configs.CHROMADB_PATH}")
            shutil.rmtree(Configs.CHROMADB_PATH)
        
        # Create a new database.
        print(f"Creating new database at {Configs.CHROMADB_PATH}")
        self.database = Chroma.from_documents(
            collection_name=Configs.CHROMA_COLLECTION_NAME, 
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=Configs.CHROMADB_PATH)


    # Load the database if it already exists.
    def load_database(self):

        # If the database exists, load it.
        if os.path.exists(Configs.CHROMADB_PATH):
            print(f"Loading existing database from {Configs.CHROMADB_PATH}")
            self.database = Chroma(
                collection_name=Configs.CHROMA_COLLECTION_NAME, 
                embedding_function=self.embeddings, 
                persist_directory=Configs.CHROMADB_PATH)
            return

        # If the database does not exist, get angryyyyyyyyyyyyyyyyyy
        raise Exception("database files or Collection does not exist!!! aaaaaaaaaaaaaaaaAAAAAAAAA")


    # Query the database with a given query.
    def query_database(self, query):
        results = self.database.similarity_search_with_relevance_scores(query, k=Configs.EMBEDDINGS_TOP_K)
        print(f"Found {len(results)} results.")
        return results