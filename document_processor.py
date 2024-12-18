from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from unstructured.partition.auto import partition
from configs import Configs
import os

# This class handles the processing of the documents, such as parsing the PDFs to markdown and splitting the text into chunks.
class DocumentProcessor:

    # Parse documents from PDF to markdown
    def parse_documents(self):
        print(f"Parsing PDFs from {Configs.PDFS_PATH}")

        # Create the data directory if it doesn't exist
        if not os.path.exists(Configs.DATA_PATH):
            os.makedirs(Configs.DATA_PATH)

        # Loop through the PDFs in the PDFs directory
        for pdf_file in os.listdir(Configs.PDFS_PATH):

            if pdf_file.lower().endswith('.pdf'):
                pdf_path = os.path.join(Configs.PDFS_PATH, pdf_file)
                
                # Partition the PDF file into elements with high resolution
                elements = partition(filename=pdf_path, content_type=Configs.PARSER_FROM_DATATYPE, hi_res=True)
                
                # Generate Markdown content
                markdown_content = ""

                # Add each element to the Markdown content
                for element in elements:
                    markdown_content += f"{element}\n\n"
                
                # Create a Markdown file for the PDF
                markdown_filename = os.path.splitext(pdf_file)[0] + ".md"
                markdown_path = os.path.join(Configs.DATA_PATH, markdown_filename)
                
                # Write the Markdown content to the file
                with open(markdown_path, "w", encoding="utf-8") as md_file:
                    md_file.write(markdown_content)
                
                print(f"Converted {pdf_file} to {markdown_filename}")


    # This function splits the documents into chunks, this helps the model focus more on specific chunks of text, than having to process the entire document.
    def split_text(self):
        print(f"Loading documents from {Configs.DATA_PATH}")

        # Load all documents that end with extension SPLITTER_DOC_EXTENSION
        loader = DirectoryLoader(Configs.DATA_PATH, glob=Configs.SPLITTER_DOC_EXTENSION_WILDCARD)
        documents = loader.load()
        print(f"Found {len(documents)} documents with extension {Configs.SPLITTER_DOC_EXTENSION_WILDCARD}.")

        # Initialize the RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=Configs.SPLITTER_CHUNK_SIZE,
            chunk_overlap=Configs.SPLITTER_OVERLAP,
            length_function=len,
            add_start_index=True,
        )

        # Split the documents into chunks
        chunks = splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks