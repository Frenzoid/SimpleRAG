import os
import PyPDF2

# Define folder paths as constants
PDF_FOLDER = "pdfs"
DATA_FOLDER = "data"

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def save_text_to_markdown(text, markdown_path):
    """
    Saves text to a Markdown file.

    Args:
        text (str): The text to save.
        markdown_path (str): Path to the Markdown file.
    """
    try:
        with open(markdown_path, 'w', encoding='utf-8') as md_file:
            md_file.write(text)
        print(f"Text successfully saved to {markdown_path}")
    except Exception as e:
        print(f"Error writing Markdown file: {e}")

if __name__ == "__main__":

    for filename in os.listdir(PDF_FOLDER):
        # Filenames
        pdf_filename = filename  
        markdown_filename = f"{pdf_filename.split('.')[0]}.md"

        # Full paths
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        markdown_path = os.path.join(DATA_FOLDER, markdown_filename)

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Save text to Markdown file
        if extracted_text.strip():  # Ensure there's content to save
            save_text_to_markdown(extracted_text, markdown_path)
        else:
            print("No text was extracted from the PDF.")
