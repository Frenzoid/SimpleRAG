from document_processor import DocumentProcessor
from database_manager import DatabaseManager
from llm_handler import LLMHandler

class RAGSystem:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.db_manager = DatabaseManager()
        self.llm_handler = LLMHandler()

    def run(self):
        # Load and process documents
        documents = self.doc_processor.load_documents()
        chunks = self.doc_processor.split_text(documents)

        # Initialize database
        embeddings_model = self.doc_processor.load_embeddings_model()
        database = self.db_manager.initialize_database(chunks, embeddings_model)

        # Query database and generate answer
        query = input("Enter your query: ")
        results = self.db_manager.query_database(database, query)
        prompt = self.db_manager.generate_prompt(results, query)
        
        # Generate answer from the LLM ( two implementations are provided, one using the HuggingFace pipeline and the other using the LitGPT)
        answer = self.llm_handler.generate_answer_hf(prompt)

        print(f"Answer: {answer}")

if __name__ == "__main__":
    RAGSystem().run()
