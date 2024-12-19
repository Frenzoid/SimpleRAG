from document_processor import DocumentProcessor
from database_manager import DatabaseManager
from llm_handler import LLMHandler
from configs import Configs

class RAGSystem:

    # The RAGSystem class is the main class of the system. It is responsible for running the system, which includes the following steps:
    def __init__(self):
        # We generate instances of the DocumentProcessor, DatabaseManager, and LLMHandler classes.
        self.doc_processor = DocumentProcessor()
        self.db_manager = DatabaseManager()
        self.llm_handler = LLMHandler()

    def run(self): 

        # If were preloading the Chroma database, we skip the document processing step, and we load it directly.
        if Configs.CHROMA_LOAD == False:

            # First, parse the documents to markdown ( saves them in the data directory )
            self.doc_processor.parse_documents()

            # Split the documents into chunks
            chunks = self.doc_processor.split_text()

            # Initialize database with the chukns and the embeddings model
            self.db_manager.initialize_database(chunks)
            
        else: 
            # Load the existing database
            self.db_manager.load_database()


        # Query database and generate answer
        while True:
            # Ask the user for a query
            query = input("Enter your query ( type 'exit' to exit ): ")

            # If the user types 'exit', then we exit the program.
            if query.lower() == "exit":
                print("Goodbye!")
                exit()
            
            # Query the database with the given query ( get k most similar chunks )
            results = self.db_manager.query_database(query)

            # Generate a prompt for the LLM model using the query and the results from the database.
            prompt = self.llm_handler.generate_prompt(results, query)
            
            # Generate answer from the LLM 
            answer = self.llm_handler.generate_answer_hf_pipeline(prompt)
            #answer = self.llm_handler.generate_answer_hf_tokenizer(prompt)

            print(f"LAMEGPT: \n {answer}")

if __name__ == "__main__":
    RAGSystem().run()