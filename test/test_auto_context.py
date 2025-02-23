# File: test_auto_context.py
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

    converter = PDFToMarkdownConverter(
        api_key=api_key,
        model_name="gemini-2.0-flash",
        show_logging=False,
        show_progress=True,
        auto_generate_context=True,
        show_cost=True,
        save_auto_context=True
    )
    
    # Set input PDF and output - using paths relative to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(root_dir, "resources", "pdf", "Dialogo-di-sostenibilita-tra-PMI-e-Banche.pdf")
    output_path = os.path.join(root_dir, "output", "output_autocontext.md")
    
    converter.set_local_pdf(pdf_path)
    converter.set_local_output(output_path)
    
    # Load custom context from file
    custom_context_path = os.path.join(root_dir, "prompt", "my_custom_context.md")
    custom_context = converter.load_custom_context_from_file(custom_context_path)

    # Execute conversion with context loaded from file
    markdown = await converter.convert(start_page=1, end_page=None, custom_context=custom_context)
    print("Conversion with auto-generated context completed.")

if __name__ == "__main__":
    asyncio.run(main())
