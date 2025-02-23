# File: test_azure_input.py
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
    converter.set_azure_input("azure_conn_string", "azure_container", "document.pdf")
    
    # Set output path relative to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_dir, "output", "output_from_azure.md")
    converter.set_local_output(output_path)

    markdown = await converter.convert(start_page=1, end_page=5)
    print("Conversion from Azure completed.")

if __name__ == "__main__":
    asyncio.run(main())
