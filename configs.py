# configs.py
class Configs:
    # Document Splitter
    SPLITTER_CHUNK_SIZE = 500 # Chunk size for splitting the document
    SPLITTER_OVERLAP = 100 # Overlap size for splitting the document

    # Embeddings Model
    EMBEDDINGS_MODEL = 'sentence-transformers/all-mpnet-base-v2' # Model name for the embeddings
    EMBEDDINGS_THRESHOLD = 0.5 # Threshold for the embeddings to be considered relevant

    # LLM Model
    LLM_MODEL = LLM_TOKENIZER = 'unsloth/Llama-3.2-1B-Instruct' # Model and tokenizer for the LLM
    LLM_TASK = 'text-generation' # Task for the LLM: 'text-generation', 'question-answering', 'summarization'...
    LLM_MAX_NEW_TOKENS = 300 # Maximum new number of tokens to generate
    LLM_PADDING = 'max_length' # Padding for the LLM
    LLM_RANDOM = True # Random generation for the LLM
    LLM_TEMP = 0.1 # Temperature for the random generation

    # Chroma
    CHROMA_LOAD = True # Load the Chroma database if it already exists
    EMBEDDINGS_TOP_K = 3 # Top K results to return from the Chroma database

    # Prompt Template
    PROMPT_INSTRUCTION = """
    Given this information only, where you have the document metadata, content and similarity score
    {documents}

    ------------------------------
    Answer the following question in less than 300 words:

    {question}
    """
