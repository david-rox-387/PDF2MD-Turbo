# PDF to Markdown Converter

A comprehensive Python solution for converting PDF documents into Markdown format using the Gemini 2.0 Flash generative AI model. This project supports PDFs stored locally or in Azure Blob Storage and provides flexible output options—either saving Markdown files locally or uploading them back to Azure.

---

## Overview

The `PDFToMarkdownConverter` class is engineered to offer a high degree of configurability and ease of use:

- **Input & Output Flexibility:**  
  Process PDFs from the local file system or Azure Blob Storage, and output Markdown either locally or to Azure.

- **Configurable Options:**  
  Easily enable or disable logging, progress indicators (via `tqdm`), and cost reporting to suit your workflow.

- **Robust Page Range Handling:**  
  Specify custom page ranges with automatic adjustment if the input range is invalid (e.g., negative values or pages beyond the document length).

- **Custom Context Insertion:**  
  Inject additional context into the conversion prompt using `<custom_context>...</custom_context>` tags.

- **Optional Auto-Generated Context:**  
  Enhance conversion quality by automatically generating context from the entire PDF. *(Note: While effective, this process may slow down conversion. Future improvements may include a more efficient three-page window approach.)*

- **Cost & Benchmarking:**  
  Monitor processing costs and execution time for a clear understanding of resource usage.

---

## Features

- **Dual Mode Input & Output:**  
  Seamlessly work with local files or Azure Blob Storage for both input and output operations.

- **Logging and Progress Indicators:**  
  Optional logging and progress bars to keep track of conversion status.

- **Adaptive Page Range Processing:**  
  Automatic adjustment of page ranges ensures smooth and error-free processing.

- **Prompt Customization:**  
  Easily add custom context to the conversion prompt to tailor the output.

- **Cost Monitoring:**  
  Track conversion costs, with detailed breakdowns such as cost per page.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Azure Blob Storage Support (Optional):**

   ```bash
   pip install azure-storage-blob
   ```

---

## Usage Example

Below is an example that demonstrates how to leverage **all** functionalities of the `PDFToMarkdownConverter`:

- Use a local PDF file as input (with an option to switch to Azure).
- Output the resulting Markdown to Azure Blob Storage (with an option to save locally).
- Include custom context and enable auto-generation of context.
- Benefit from logging, progress tracking, and cost reporting.

```python
import asyncio
import os
from pdf_to_markdown_converter import PDFToMarkdownConverter

async def main():
    # Retrieve the Gemini API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set.")
        return

    # Initialize the converter with full functionality enabled
    converter = PDFToMarkdownConverter(
        api_key=api_key,
        show_logging=True,
        show_progress=True,
        auto_generate_context=True,
        show_cost=True
    )
    
    # --- Input Configuration ---
    # Option 1: Local PDF file
    converter.set_local_pdf("sample_document.pdf")
    # Option 2: Azure Blob Storage input (uncomment to enable)
    # converter.set_azure_input("azure_input_connection_string", "input_container", "sample_document.pdf")
    
    # --- Output Configuration ---
    # Option 1: Upload the Markdown output to Azure Blob Storage
    converter.set_azure_output("azure_output_connection_string", "output_container", "output_document.md")
    # Option 2: Save output locally (uncomment to enable)
    # converter.set_local_output("output_document.md")
    
    # --- Conversion Settings ---
    start_page = 1
    end_page = 10  # Automatically adjusted if exceeding document length
    custom_context = "This is a custom context provided by the user."
    
    # Perform the conversion
    markdown = await converter.convert(start_page=start_page, end_page=end_page, custom_context=custom_context)
    
    print("Conversion completed.")
    # You can further process the 'markdown' variable if needed.
    # print(markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Test Scripts

Several test scripts are included to validate different configurations and scenarios:

1. **Local Conversion Test**  
   - **File:** `test_local_conversion.py`  
   - **Description:** Converts a local PDF to Markdown, inserting custom context, and saves the result locally.

2. **Azure Input Test**  
   - **File:** `test_azure_input.py`  
   - **Description:** Downloads a PDF from Azure Blob Storage, converts it to Markdown, and saves the output locally.

3. **Azure Output Test**  
   - **File:** `test_azure_output.py`  
   - **Description:** Converts a local PDF to Markdown and uploads the output to Azure Blob Storage.

4. **Auto-Context Generation Test**  
   - **File:** `test_auto_context.py`  
   - **Description:** Uses the auto-generation feature to create context from the entire PDF before conversion. *(Initial tests demonstrated the feasibility of auto-generated context, though it can be time-consuming. Future work may explore processing a three-page window for improved efficiency.)*

---

## Future Improvements

- **Context Optimization:**  
  Explore a tri-page window approach (using the middle page) to efficiently extract context without processing the entire document.

- **Performance Enhancements:**  
  Optimize asynchronous processing for large PDFs to further reduce conversion times.

---

## Conclusion

This project delivers a robust and flexible solution for converting PDFs to Markdown. By combining customizable prompts, advanced context generation, and comprehensive logging and cost reporting, it offers a professional tool for document conversion. Whether working locally or in a cloud environment with Azure, this solution is designed to meet diverse needs while maintaining clarity and efficiency.

---

## Code Overview

The core of the project is the `PDFToMarkdownConverter` class, which provides:

- **Input Handling:**  
  Supports PDF inputs from local files and Azure Blob Storage.

- **Output Management:**  
  Outputs Markdown either as a local file or via Azure Blob Storage upload.

- **PDF Processing:**  
  Utilizes PyPDF2 to extract and process PDF content.

- **Conversion Engine:**  
  Converts PDF pages to Markdown using the Gemini 2.0 Flash AI model, with optional auto-generated context.

- **Additional Utilities:**  
  Includes logging, progress bars (via `tqdm`), and cost monitoring for enhanced user feedback.

Test scripts accompany the project to demonstrate various configurations and ensure robust functionality across different environments.
