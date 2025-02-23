# File: test_local_conversion.py
import asyncio
import os
from pdf_to_markdown_converter import PDFToMarkdownConverter

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
    converter.set_local_pdf("document.pdf")
    converter.set_local_output("output.md")

    # Specify page range and custom context
    markdown = await converter.convert(start_page=1, end_page=10, custom_context="Custom user context.")
    print("Conversion completed.")

if __name__ == "__main__":
    asyncio.run(main())
