# PDF To Markdown Converter

This project implements a flexible and efficient Python class to convert PDF documents into Markdown format using a generative AI model (Gemini 2.0 Flash). It supports both local files and Azure Blob Storage for input, as well as local and Azure outputs for the Markdown results.

## Overview

The `PDFToMarkdownConverter` class is designed with a variety of configurable options to meet different needs:
- **Input/Output Flexibility:** Process PDFs from a local file system or Azure Blob Storage, and output the converted Markdown either locally or back to Azure.
- **Configurable Options:** Toggle logging, progress bar display (using `tqdm`), and cost reporting.
- **Page Range Handling:** Specify page ranges with automatic adjustments if the provided range is out of bounds (e.g., negative values or values exceeding the total number of pages).
- **Custom Context Insertion:** Insert a custom context (wrapped in `<custom_context>...</custom_context>`) into the conversion prompt.
- **Context Auto-Generation:** Optionally generate context from the entire PDF text. *(Note: This method was tested by adding context every time, but it resulted in long processing times and proved inefficient. An interesting alternative would be to process a window of three pages and use the middle page to maintain context while reducing overhead. For now, this remains the best solution available.)*
- **Cost & Benchmarking:** Optionally display the cost and execution time for the conversion process.

## Features

- **Local & Azure Support:** Seamlessly work with PDFs stored locally or in Azure Blob Storage.
- **Logging & Progress Indicators:** Enable logging and progress bars for better tracking during conversion.
- **Robust Page Range Processing:** Automatically adjust invalid page ranges to ensure smooth processing.
- **Prompt Customization:** Easily inject additional context into the conversion prompt.
- **Auto-Generated Context (Optional):** Enhance the conversion prompt by generating context from the full document.
- **Cost Monitoring:** Log the processing cost and timing for each conversion task.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/david-rox-387/PDF2MD-Turbo
   cd your-repo-directory
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For Azure support, install the Azure Blob Storage SDK:
   ```bash
   pip install azure-storage-blob
   ```

## Usage Example

Below is an example that demonstrates how to use **all** functionalities of the `PDFToMarkdownConverter`, including:
- Local input (with an option to switch to Azure input)
- Azure output (with an option to switch to local output)
- Custom context insertion
- Auto-generation of context from the PDF
- Logging, progress bar display, and cost reporting

```python
import asyncio
import os
from pdf_to_markdown_converter import PDFToMarkdownConverter

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set.")
        return

    # Initialize the converter with all functionalities enabled.
    converter = PDFToMarkdownConverter(
        api_key=api_key,
        show_logging=True,
        show_progress=True,
        auto_generate_context=True,
        show_cost=True
    )
    
    # -------------------------------
    # Input configuration:
    # Option 1: Local PDF file
    converter.set_local_pdf("sample_document.pdf")
    # Option 2 (uncomment to use Azure Blob for input):
    # converter.set_azure_input("azure_input_connection_string", "input_container", "sample_document.pdf")
    
    # -------------------------------
    # Output configuration:
    # Option 1: Upload the Markdown output to Azure Blob Storage
    converter.set_azure_output("azure_output_connection_string", "output_container", "output_document.md")
    # Option 2 (uncomment to save locally):
    # converter.set_local_output("output_document.md")
    
    # -------------------------------
    # Conversion settings:
    start_page = 1
    end_page = 10  # If end_page exceeds the document length, it is adjusted automatically.
    custom_context = "This is a custom context provided by the user."
    
    # Perform the conversion.
    markdown = await converter.convert(start_page=start_page, end_page=end_page, custom_context=custom_context)
    
    print("Conversion completed.")
    # If the output mode is set to "string", you can also print or further process the 'markdown' variable.
    # print(markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

## Test Scripts

The following test scripts have been created to validate different configurations and usage scenarios:

1. **Local Conversion Test (Local PDF Input, Local File Output)**
   - **File:** `test_local_conversion.py`
   - **Description:** Converts a local PDF to Markdown and saves the output locally. This test includes the insertion of a custom context.

2. **Azure Input Test (Azure PDF Input, Local File Output)**
   - **File:** `test_azure_input.py`
   - **Description:** Downloads a PDF from Azure Blob Storage, converts it to Markdown, and saves the result locally.

3. **Azure Output Test (Local PDF Input, Azure Output)**
   - **File:** `test_azure_output.py`
   - **Description:** Converts a local PDF to Markdown and uploads the output to Azure Blob Storage.

4. **Auto-Context Generation Test**
   - **File:** `test_auto_context.py`
   - **Description:** Uses the auto-generation feature to create context from the entire PDF before conversion. Initial tests used a system that added context for every conversion, but this approach proved too time-consuming. An interesting future enhancement would be to process three pages at a time and focus on the middle one to maintain context more efficiently. For now, this solution is the best balance between context quality and processing time.

## Future Improvements

While this solution is robust and flexible, there is room for further enhancement:
- **Context Optimization:** Investigate a tri-page window approach (using the middle page) to extract context efficiently without processing the entire document.
- **Performance Enhancements:** Further optimize asynchronous processing, especially for large PDFs, to reduce conversion time.

## Conclusion

This project represents a comprehensive and flexible solution for converting PDF documents to Markdown. Despite the challenges with auto-generated context (which, although effective, can be slow), this implementation is the best solution currently available. Future improvements will aim to refine context generation and further optimize performance.
