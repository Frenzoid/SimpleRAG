# SimpleRAG

SimpleRAG is an implementation of Retrieval-Augmented Generation (RAG) using Python. RAG enhances the capabilities of generative language models by integrating retrieval-based methods to provide more contextually relevant responses.

## Overview

Retrieval-Augmented Generation (RAG) combines retrieval-based techniques with generative language models to improve response quality by retrieving relevant information from a knowledge source before generating responses. This implementation leverages Python for processing and managing the integration between retrieval mechanisms and language generation models, and doesn't require or use of any authentication token with Meta, Huggignface, or else.

## Features

- **Document Processing**: Extracts and processes text from PDF documents to build a knowledge base using Unstructured, in the example were using as dataset a Linux manual book and the entire AWS Serverless Documentation.
- **Database Management**: Stores and manages a vectorial database for the processed documents for efficient retrieval using ChromaDB.
- **Language Model Handling**: Integrates with language models to generate responses augmented with retrieved information, in the example we are using Llama-3.2-3B-Instruct.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Frenzoid/SimpleRAG.git
   cd SimpleRAG
   ```
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the environment**:

   Ensure that all necessary configurations are set in `configs.py`.

## Usage

**Run the Main Application**:

   Just start the main application:

```bash
   python main.py
```

   This will initialize the system, allowing it to handle queries using the RAG approach.
   After this initial run, you may want to set `CHROMA_LOAD` on `configs.py` to `False`, so next runs will load the dataset instead of recreating the entire thing.

## Sample Output and interaction

```
⚡ ~ python main.py
Loading embeddings model: sentence-transformers/all-mpnet-base-v2
Loading LLM model: unsloth/Llama-3.2-3B-Instruct
Device set to use cpu
Parsing PDFs from pdfs
Converted The_Linux_Users_Guide.pdf to The_Linux_Users_Guide.md
Converted serverless-core.pdf to serverless-core.md
Loading documents from data
Found 2 documents with extension *md.
Split 2 documents into 1347 chunks.
Deleting old database at chroma
Creating new database at chroma
Enter your query ( type 'exit' to exit ): what is IAM in AWS?
Found 6 results.
Generating answer using model: unsloth/Llama-3.2-3B-Instruct, method HUGGINFACE PIPELINE
LAMEGPT: 

AWS Identity and Access Management (IAM) is a service that helps you securely control access to AWS resources. It allows you to manage users, groups, roles, and their permissions. IAM enables fine-grained access by defining policies to specify which actions are allowed or denied for specific resources. With features like multi-factor authentication (MFA) and temporary credentials, IAM enhances security. It supports identity federation, allowing external users to access AWS without creating IAM users. IAM is essential for managing secure access and ensuring compliance in AWS environments.
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Frenzoid/SimpleRAG/blob/master/LICENSE) file for details.

## Acknowledgments

This project utilizes various open-source libraries and models. We thank the contributors of these projects for their hard work.

For more information, visit the [GitHub repository](https://github.com/Frenzoid/SimpleRAG).
