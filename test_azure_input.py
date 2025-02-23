# File: test_azure_input.py
import asyncio
import os
from dotenv import load_dotenv
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
    converter.set_local_output("output_from_azure.md")

    markdown = await converter.convert(start_page=1, end_page=5)
    print("Conversion from Azure completed.")

if __name__ == "__main__":
    asyncio.run(main())
