# File: test_azure_output.py
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
    converter.set_local_pdf("document.pdf")
    converter.set_azure_output("azure_conn_string", "azure_output_container", "output_document.md")

    markdown = await converter.convert(start_page=1, end_page=10)
    print("Conversion completed and output uploaded to Azure.")

if __name__ == "__main__":
    asyncio.run(main())
