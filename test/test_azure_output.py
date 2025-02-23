# File: test_azure_output.py
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to Python path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_to_markdown_converter import PDFToMarkdownConverter

# Load environment variables from .env file
load_dotenv()

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set.")
        return

    converter = PDFToMarkdownConverter(api_key)
    
    # Set input path relative to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(root_dir, "resources", "pdf", "document.pdf")
    converter.set_local_pdf(input_path)
    
    converter.set_azure_output("azure_conn_string", "azure_output_container", "output_document.md")

    markdown = await converter.convert(start_page=1, end_page=10)
    print("Conversion completed and output uploaded to Azure.")

if __name__ == "__main__":
    asyncio.run(main())
