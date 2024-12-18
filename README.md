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
Loading documents from data
Found 2 documents.
Split 2 documents into 785 chunks.
Loading embeddings model: sentence-transformers/all-mpnet-base-v2
Loading existing database from chroma
Enter your query: What is IAM in AWS?
Found 3 results.
Generating answer using model: meta-llama/Llama-3.1-8B, method HUGGINFACE PIPELINE
Loading checkpoint shards: 100%|██████████████████████████████████████████████████████████████████████| 4/4 [00:02<00:00,  1.61it/s]
Device set to use cpu
Answer:

    Identity and Access Management (IAM) is a service that helps an administrator securely control access to AWS resources. IAM administrators control who can be authenticated (i.e. who has an identity), and who has permission (i.e. authorization) to do what. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate use
rs. Instead, IAM works with your identity provider (IdP) to authenticate users. IAM works with your IdP to authenticate users. IAM is an authorization service. IAM does not authenticate users. Instead, IAM works with your identity
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Frenzoid/SimpleRAG/blob/master/LICENSE) file for details.

## Acknowledgments

This project utilizes various open-source libraries and models. We thank the contributors of these projects for their hard work.

For more information, visit the [GitHub repository](https://github.com/Frenzoid/SimpleRAG).
