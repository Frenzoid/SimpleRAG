import os
import shutil
from langchain_chroma import Chroma
from configs import Configs

# This class handles the database operations, such as initializing the database, querying the database, and generating the prompt.
class DatabaseManager:
    
    # Initialize the database, either by loading an existing database or creating a new one.
    def initialize_database(self, chunks, embeddings_model):

        # If the database already exists, and we want to load it, then load it.
        if os.path.exists(Configs.CHROMADB_PATH) and Configs.CHROMA_LOAD:
            print(f"Loading existing database from {Configs.CHROMADB_PATH}")
            return Chroma(embedding_function=embeddings_model, persist_directory=Configs.CHROMADB_PATH)

        # If the database already exists, but we want to overwrite it, then delete it.
        if os.path.exists(Configs.CHROMADB_PATH):
            print(f"Deleting old database at {Configs.CHROMADB_PATH}")
            shutil.rmtree(Configs.CHROMADB_PATH)
        
        print(f"Creating new database at {Configs.CHROMADB_PATH}")
        return Chroma.from_documents(chunks, embedding=embeddings_model, persist_directory=Configs.CHROMADB_PATH)
    
    # Query the database with a given query.
    def query_database(self, database, query):
        results = database.similarity_search_with_relevance_scores(query, k=Configs.EMBEDDINGS_TOP_K)
        print(f"Found {len(results)} results.")
        return results

    # Generate a prompt for the LLM model using the query and the results from the database.
    def generate_prompt(self, results, query):
        # If there are no results, or the score of the results are below the threshold, return an empty string.
        if not results or results[0][1] < Configs.EMBEDDINGS_THRESHOLD:
            return "Tell the user that there are no relevant documents found for the query."

        documents_str = "\n".join([f"Document: {doc.metadata}\nContent: {doc.page_content}\nScore: {score}" for doc, score in results])
        return Configs.PROMPT_INSTRUCTION.format(documents=documents_str, question=query)
