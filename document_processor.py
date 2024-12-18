from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from configs import Configs

class DocumentProcessor:
    
    # This function loads the markdown documents from the data directory.    
    def load_documents(self):
        print(f"Loading documents from {Configs.DATA_PATH}")
        loader = DirectoryLoader(Configs.DATA_PATH, glob='*.md')
        documents = loader.load()
        print(f"Found {len(documents)} documents.")
        return documents

    # This function splits the documents into chunks, this helps the model focus more on specific chunks of text, than having to process the entire document.
    def split_text(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=Configs.SPLITTER_CHUNK_SIZE,
            chunk_overlap=Configs.SPLITTER_OVERLAP,
            length_function=len,
            add_start_index=True,
        )
        chunks = splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

    # This function loads the embeddings model from HuggingFace.
    def load_embeddings_model(self):
        print(f"Loading embeddings model: {Configs.EMBEDDINGS_MODEL}")
        return HuggingFaceEmbeddings(model_name=Configs.EMBEDDINGS_MODEL)
