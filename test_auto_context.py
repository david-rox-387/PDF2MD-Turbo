# File: test_auto_context.py
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

    converter = PDFToMarkdownConverter(
        api_key=api_key,
        model_name="gemini-2.0-flash",
        show_logging=False,
        show_progress=True,
        auto_generate_context=True,
        show_cost=True,
        save_auto_context=True
    )
    
    # Set input PDF and output
    converter.set_local_pdf("resources/pdf/Dialogo-di-sostenibilita-tra-PMI-e-Banche.pdf")
    converter.set_local_output("output/output_autocontext.md")
    
    # Load custom context from file
    custom_context_path = os.path.join(os.path.dirname(__file__), "prompt", "my_custom_context.md")
    custom_context = converter.load_custom_context_from_file(custom_context_path)

    # Execute conversion with context loaded from file
    markdown = await converter.convert(start_page=1, end_page=3, custom_context=custom_context)
    print("Conversion with auto-generated context completed.")

if __name__ == "__main__":
    asyncio.run(main())
