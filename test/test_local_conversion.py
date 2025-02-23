# File: test_local_conversion.py
import asyncio
import os
import sys
from dotenv import load_dotenv
from pdf_to_markdown_converter import PDFToMarkdownConverter

# Add parent directory to Python path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set.")
        return

    converter = PDFToMarkdownConverter(
        api_key,
        show_logging=True,
        show_progress=True,
        auto_generate_context=False,
        show_cost=True
    )
    
    # Set input and output paths relative to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(root_dir, "resources", "pdf", "document.pdf")
    output_path = os.path.join(root_dir, "output", "output.md")
    
    converter.set_local_pdf(input_path)
    converter.set_local_output(output_path)

    # Specify page range and custom context
    markdown = await converter.convert(start_page=1, end_page=10, custom_context="Custom user context.")
    print("Conversion completed.")

if __name__ == "__main__":
    asyncio.run(main())
