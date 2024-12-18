# configs.py
class Configs:
    # Paths
    PDFS_PATH = "pdfs"
    DATA_PATH = 'data'
    CHROMADB_PATH = 'chroma'
    LLM_PATH = 'llmmodel'
    
    # Document Splitter
    PARSER_FROM_DATATYPE = "application/pdf"
    SPLITTER_DOC_EXTENSION_WILDCARD = "*md" # Document format for the splitter
    SPLITTER_CHUNK_SIZE = 500 # Chunk size for splitting the document
    SPLITTER_OVERLAP = 100 # Overlap size for splitting the document

    # Embeddings Model
    EMBEDDINGS_MODEL = 'sentence-transformers/all-mpnet-base-v2' # Model name for the embeddings
    EMBEDDINGS_THRESHOLD = 0.5 # Threshold for the embeddings to be considered relevant

    # LLM Model ( Best models are Instruct with GGUF and 4b, check https://huggingface.co/collections/unsloth/4bit-instruct-models-6624b1c17fd76cbcf4d435c8 )
    LLM_MODEL = LLM_TOKENIZER = 'unsloth/Llama-3.2-3B-Instruct' # Model and tokenizer for the LLM ( usually the same if using HuggingFace models )
    LLM_TASK = 'text-generation' # Task for the LLM: 'text-generation', 'question-answering', 'summarization'...
    LLM_MAX_NEW_TOKENS = 2048 # Maximum new number of tokens to generate
    LLM_PADDING = 'max_length' # Padding for the LLM
    LLM_RANDOM = True # Random generation for the LLM
    LLM_TEMP = 0.4 # Temperature for the random generation
    LLM_RETURN_FULL_TEXT = False # Add the system propmt to the returned text

    # Database
    CHROMA_LOAD = False # Load the Chroma database if it already exists
    CHROMA_COLLECTION_NAME = "Collection1" # Default collection ( database ) name for the Chroma database
    # Embeddings
    EMBEDDINGS_TOP_K = 6 # Top K results to return from the Chroma database

    # Prompt Template
    PROMPT_INSTRUCTION = """
    Given this information only, where you have the document's metadata, content and similarity score


    {documents}

    Answer the following question in less than 300 words:

    {question}
    """
