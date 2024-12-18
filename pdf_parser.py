import os
from unstructured.partition.auto import partition
from configs import Configs

def parse_pdfs_to_markdown():

    for pdf_file in os.listdir(Configs.PDFS_PATH):
        if pdf_file.lower().endswith('.pdf'):
            pdf_path = os.path.join(Configs.PDFS_PATH, pdf_file)
            
            # Partition the PDF file into elements with high resolution
            elements = partition(filename=pdf_path, content_type="application/pdf", hi_res=True)
            
            # Generate Markdown content
            markdown_content = ""
            for element in elements:
                markdown_content += f"{element}\n\n"
            
            # Create a Markdown file for the PDF
            markdown_filename = os.path.splitext(pdf_file)[0] + ".md"
            markdown_path = os.path.join(Configs.DATA_PATH, markdown_filename)
            
            with open(markdown_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
            
            print(f"Converted {pdf_file} to {markdown_filename}")

# Run the function
if __name__ == "__main__":
    
    # Ensure the output directory exists
    os.makedirs(Configs.DATA_PATH, exist_ok=True)
    parse_pdfs_to_markdown()