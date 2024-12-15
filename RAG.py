# Langchain imports
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings

# Huggingface imports
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# System imports
import os
import shutil


# PATHS
DATA_PATH = 'data'
CHROMADB_PATH = 'chroma'

# DOC SPLITTER
SPLITTER_CHUNK_SIZE = 1000
SPLITTER_OVERLAP = 300

# MODELS 
EMBEDDINGS_MODEL = 'sentence-transformers/all-mpnet-base-v2'
EMBEDDINGS_TOP_K = 3
LLM_MODEL = LLM_TOKENIZER = 'EleutherAI/gpt-j-6b' # model and tokenizer are the same because they are from the same model
LLM_MAX_LENGTH = 512
LLM_PADDING = 'max_length'
LLM_RANDOM = True # Should the LLM generate random answers? True or False
LLM_TEMP = 0.5 # Temperature for the random generation
LLM_TASK = 'text-generation' # 'text-generation', 'question-answering'
LLM_PATH = 'llmmodel'

# PROMT
PROMT_INSTRUCTION = """
Given this information only, where you have the document metadata, content and similarity score
{documents}

------------------------------
Answer the following question:

{question}
"""

# Load the documents
def load_documents():
    """ We load the documents from the data directory. """

    # Print the path to the data directory
    print(f"load_documents: Loading documents from {DATA_PATH}")

    # Load all documents from the data directory finishing with .md
    loader = DirectoryLoader(DATA_PATH, glob='*.md')

    # Load the documents
    documents = loader.load()

    # Print the number of documents found
    print(f"load_documents: Found {len(documents)} documents.")

    # Return documents
    return documents

# Load the documents
def split_text(documents: list[Document]):
    """ We split the documents into chunks of 300 characters with 100 characters overlap,
    we do this because splitting helps the model focus more on specific chunks of text, than
    having to process the entire document"""

    # Print the number of documents
    print(f"split_text: Splitting {len(documents)} documents into {SPLITTER_CHUNK_SIZE} character chunks with {SPLITTER_OVERLAP} character overlap.")

    # Split the text into chunks of 300 characters with 100 characters overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=SPLITTER_CHUNK_SIZE,
        chunk_overlap=SPLITTER_OVERLAP,
        length_function=len,
        add_start_index=True,
    )

    # Split the documents into chunks
    chunks = text_splitter.split_documents(documents)
    print(f"split_text: Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

# load embeddings model from hugginface
def load_embeddings_model():
    """ We load the embeddings model from HuggingFace. """
    
    # Print the model name
    print(f"load_embeddings_model: Loading embeddings model {EMBEDDINGS_MODEL} from HuggingFace.")

    # Embeddings model name
    model = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

    # Print the model name
    print(f"load_embeddings_model: Loaded embeddings model {model.model_name}.")
    
    return model


# Create virtual chroma database
def init_chroma_database(chunks: list[Document], embeddings_model: HuggingFaceEmbeddings):
    """ We create a virtual Chroma database from the chunks of text, and the embeddings model,
    this database will be used to query the most similar chunks of text to a given query by the user,
    and later on used by the LLM to generate the final answer. """

    # Print the path to the chroma database
    print(f"init_chroma_database: Creating a Chroma database at path: {CHROMADB_PATH}")

    # Delete the dataset if it already exists
    if os.path.exists(CHROMADB_PATH):
        print(f"init_chroma_database: Overwritting pre-existing Chroma database at path: {CHROMADB_PATH}")
        shutil.rmtree(CHROMADB_PATH)
    else:
        print(f"init_chroma_database: Creating a new Chroma database at path: {CHROMADB_PATH}")

    # Create a new sqlite database to store vectorial representations of the documents
    database = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings_model, 
        persist_directory=CHROMADB_PATH)

    # Print the number of documents in the database
    print(f"init_chroma_database: Created a Chroma database with {len(database)} documents.")

    return database

# Query the chroma database
def query_chroma_database(embeddings_model: HuggingFaceEmbeddings, database: Chroma):
    """ We query the Chroma database with a given query, the database will return the most k similar
    chunks of text to the query. """

    # Print the query
    print(f"query_chroma_database: Querying the Chroma database")

    # Ask the user for a query
    query = input("query_chroma_database > Enter a query to search the database: ")

    # Query the database, returns a list of tuples with the document and the similarity score
    results = database.similarity_search_with_relevance_scores(query, k=3)

    # Print the number of results
    print(f"query_chroma_database: Found {len(results)} results.")

    return query, results

# Generate full operator promt
def op_promt(chunks: list[tuple[Document, float]], question: str):
    """ We generate a full operator promt with the documents and the question. """

    # Print status
    print(f"op_promt: Generating operator with {len(chunks)} documents and question:{question}")

    # Create a string with the documents
    documents_str = "\n".join([f"\n\nDocument: {doc.metadata}\nContent: {doc.page_content}\nScore: {score}" for (doc, score) in chunks])

    # Return the promt
    print(f"op_promt: Generated operator promt.")
    return PROMT_INSTRUCTION.format(documents=documents_str, question=question)

# Have the LLM generate the final answer
def generate_answer(promt: str):
    """ We generate the final answer using the LLM model. """

    # Print status
    print("generate_answer: Generating answer using the LLM model.")

    # Load the LLM model
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL, cache_dir=LLM_PATH)
    tokenizer = AutoTokenizer.from_pretrained(LLM_TOKENIZER, cache_dir=LLM_PATH)

    # Create an generator ( pipeline instance ) with the LLM model, retruns a TextGenerationPipeline
    generator = pipeline(
        task=LLM_TASK, 
        model=model, 
        tokenizer=tokenizer)

    # Query the pipeline (model with speific parameters) for a text generation, returns a list or a list of lists of dict
    #   https://huggingface.co/docs/transformers/v4.47.1/en/main_classes/pipelines#transformers.TextGenerationPipeline
    answers = generator(
        promt, 
        max_length=LLM_MAX_LENGTH,
        truncation=True,
        padding=LLM_PADDING,
        do_sample=LLM_RANDOM, 
        temperature=LLM_TEMP, 
        return_full_text=False)

    # Print status
    print(f"generate_answer: Generated answer")

    return answers

# Main function
def main():

    # Load the documents
    documents = load_documents()

    # Split the documents into chunks
    document_chunks = split_text(documents)

    # Load the embeddings model
    embeddings_model = load_embeddings_model()

    # Create a virtual chroma database
    database_instance = init_chroma_database(document_chunks, embeddings_model)

    # Query the chroma database
    query, results = query_chroma_database(embeddings_model, database_instance)

    """
    # DEBUG: Print the top k similar results from the database    
    print("Results:")
    for i, (doc, score) in enumerate(results):
        print(f"Result {i+1}:")
        print(f"Score: {score}")
        print(f"Text: {doc.page_content}")
        print(f"Document: {doc.metadata}")
        print("\n")"""

    # Generate the final system promt
    system_promt = op_promt(results, query)

    """
    # DEBUG: Print the operator promt
    print(system_promt)
    """

    # Generate the final answer
    answer = generate_answer(system_promt)
    print(f"\n\nAnswer: {answer[0]['generated_text']}")

# Run the main function
if __name__ == '__main__':
    main()