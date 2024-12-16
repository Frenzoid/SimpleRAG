
# SimpleRAG

SimpleRAG is an implementation of Retrieval-Augmented Generation (RAG) using Python. RAG enhances the capabilities of generative language models by integrating retrieval-based methods to provide more contextually relevant responses.

## Overview

Retrieval-Augmented Generation (RAG) combines retrieval-based techniques with generative language models to improve response quality by retrieving relevant information from a knowledge source before generating responses. This implementation leverages Python for processing and managing the integration between retrieval mechanisms and language generation models.

## Features

- **Document Processing**: Extracts and processes text from PDF documents to build a knowledge base.
- **Database Management**: Stores and manages processed documents for efficient retrieval.
- **Language Model Handling**: Integrates with language models to generate responses augmented with retrieved information.

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

1. **Process Documents**:

   Place your PDF documents in the `pdfs` directory.

   Run the document processor to extract and store text:

   ```bash
   python document_processor.py
   ```

2. **Run the Main Application**:

   Start the main application:

   ```bash
   python main.py
   ```

   This will initialize the system, allowing it to handle queries using the RAG approach.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Frenzoid/SimpleRAG/blob/master/LICENSE) file for details.

## Acknowledgments

This project utilizes various open-source libraries and models. We thank the contributors of these projects for their hard work.

For more information, visit the [GitHub repository](https://github.com/Frenzoid/SimpleRAG).
