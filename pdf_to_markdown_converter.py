import os
import asyncio
import logging
import time
from io import BytesIO
from typing import Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
import google.generativeai as genai

# Conditional Azure import
try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

class PDFToMarkdownConverter:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.0-flash",
        show_logging: bool = True,
        show_progress: bool = True,
        auto_generate_context: bool = False,
        show_cost: bool = False,
        save_auto_context: bool = False
    ):
        """
        Initialize the converter.
        
        :param api_key: API key for Gemini.
        :param model_name: Model name to use.
        :param show_logging: Whether to enable logging.
        :param show_progress: Whether to show progress bar (tqdm).
        :param auto_generate_context: Whether to auto-generate context by analyzing the entire PDF.
        :param show_cost: Whether to show conversion cost (and time), including auto-generation phase.
        :param save_auto_context: Whether to save auto-generated context to a file.
        """
        if not api_key:
            raise ValueError("API key not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        self.show_logging = show_logging
        self.show_progress = show_progress
        self.auto_generate_context = auto_generate_context
        self.show_cost = show_cost
        self.save_auto_context = save_auto_context
        self._auto_context = None  # Store the auto-generated context

        # Configure logger
        self.logger = logging.getLogger(__name__)
        if self.show_logging:
            logging_level = os.getenv("LOG_LEVEL", "INFO").upper()
            logging.basicConfig(level=logging_level)
        else:
            logging.basicConfig(level=logging.CRITICAL)

        # Input settings
        self.input_mode = "local"  # "local" or "azure"
        self.pdf_path: Optional[str] = None
        self.azure_input_connection_string: Optional[str] = None
        self.azure_input_container: Optional[str] = None

        # Output settings
        self.output_mode = "string"  # "string", "local" or "azure"
        self.output_path: Optional[str] = None
        self.azure_output_connection_string: Optional[str] = None
        self.azure_output_container: Optional[str] = None
        self.azure_output_blob: Optional[str] = None

    # --- Methods for setting PDF input ---
    def set_local_pdf(self, pdf_path: str):
        """Set PDF from local file."""
        self.pdf_path = pdf_path
        self.input_mode = "local"

    def set_azure_input(self, connection_string: str, container_name: str, blob_name: str):
        """Set PDF from Azure Blob Storage."""
        if not AZURE_AVAILABLE:
            raise ImportError("Azure Storage Blob SDK not installed. Run 'pip install azure-storage-blob'")
        self.azure_input_connection_string = connection_string
        self.azure_input_container = container_name
        self.pdf_path = blob_name
        self.input_mode = "azure"

    # --- Methods for setting output ---
    def _ensure_directory_exists(self, file_path: str):
        """Ensure that the directory for file_path exists, creating it if necessary."""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"Created directory: {directory}")
            except Exception as e:
                self.logger.error(f"Error creating directory {directory}: {e}")
                raise

    def set_local_output(self, output_path: str):
        """Set output to local file."""
        self.output_mode = "local"
        self.output_path = output_path
        # Ensure output directory exists
        self._ensure_directory_exists(output_path)

    def set_azure_output(self, connection_string: str, container_name: str, blob_name: str):
        """Set output to Azure Blob Storage."""
        if not AZURE_AVAILABLE:
            raise ImportError("Azure Storage Blob SDK not installed. Run 'pip install azure-storage-blob'")
        self.output_mode = "azure"
        self.azure_output_connection_string = connection_string
        self.azure_output_container = container_name
        self.azure_output_blob = blob_name

    # --- Internal methods for PDF handling ---
    def _download_pdf(self) -> bytes:
        """Retrieve PDF (from local or Azure)."""
        if self.input_mode == "azure":
            blob_service_client = BlobServiceClient.from_connection_string(self.azure_input_connection_string)
            container_client = blob_service_client.get_container_client(self.azure_input_container)
            blob_client = container_client.get_blob_client(self.pdf_path)
            download_stream = blob_client.download_blob()
            data = download_stream.readall()
            return data
        else:
            with open(self.pdf_path, "rb") as f:
                return f.read()

    def _upload_output_to_azure(self, content: str):
        """Upload Markdown output to Azure Blob Storage."""
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_output_connection_string)
        container_client = blob_service_client.get_container_client(self.azure_output_container)
        blob_client = container_client.get_blob_client(self.azure_output_blob)
        blob_client.upload_blob(content, overwrite=True)
        self.logger.info(f"Output uploaded to Azure Blob: {self.azure_output_blob}")

    def _load_prompt_template(self) -> str:
        """Load prompt template from file (prompt_template.md)."""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt", "prompt_template.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Prompt file not found: {prompt_path}")
            raise

    def _load_auto_context_template(self) -> str:
        """Load auto-context template from file (auto_custom_context.md)."""
        template_path = os.path.join(os.path.dirname(__file__), "prompt", "auto_custom_context.md")
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Auto-context template file not found: {template_path}")
            raise

    def _save_auto_context(self, context: str):
        """Save auto-generated context to a markdown file."""
        if not self.save_auto_context:
            return
            
        output_dir = os.path.join(os.path.dirname(__file__), "prompt")
        # Ensure directory exists
        self._ensure_directory_exists(output_dir)
        
        # Get PDF filename without extension
        pdf_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        output_filename = f"{pdf_name}_auto_context_generated.md"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(context)
            self.logger.info(f"Auto-generated context saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving auto-generated context: {e}")

    def load_custom_context_from_file(self, context_path: str) -> str:
        """Load custom context from a markdown file."""
        try:
            with open(context_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Custom context file not found: {context_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading custom context: {e}")
            raise

    # --- Auto-generation of context ---
    async def _auto_generate_context(self, pdf_text: str) -> Tuple[str, float, float]:
        """
        Execute context auto-generation by passing the entire PDF text.
        
        Returns a tuple: (context_text, cost, time_taken)
        """
        # Load template and replace filename
        template = self._load_auto_context_template()
        file_name = os.path.basename(self.pdf_path)
        template = template.replace('"{file_name}"', f'"{file_name}"')
        
        # Add PDF text to template
        auto_prompt = template + "\n" + pdf_text
        
        start_time = time.time()
        response = await asyncio.to_thread(self.model.generate_content, auto_prompt)
        elapsed = time.time() - start_time
        cost = getattr(response, "cost", 0)
        if self.show_cost:
            self.logger.info(f"Auto-generated context: cost = {cost}, time = {elapsed:.2f}s")
        
        # Save auto-generated context
        self._save_auto_context(response.text)
        
        return response.text, cost, elapsed

    # --- Processing a single page ---
    async def _process_page(self, reader: PdfReader, page_num: int, final_prompt: str) -> Tuple[str, float]:
        """
        Process a single PDF page.
        
        Returns a tuple (markdown_text, page_cost).
        """
        self.logger.info(f"Processing page {page_num}...")
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num - 1])
        buffer = BytesIO()
        writer.write(buffer)
        page_data = buffer.getvalue()
        buffer.close()

        response = await asyncio.to_thread(
            self.model.generate_content,
            [final_prompt, {"mime_type": "application/pdf", "data": page_data}]
        )
        page_cost = getattr(response, "cost", 0)
        return response.text, page_cost

    # --- Main conversion method ---
    async def convert(
        self,
        start_page: int = 1,
        end_page: Optional[int] = None,
        custom_context: Optional[str] = None
    ) -> str:
        """
        Convert PDF to Markdown.

        :param start_page: Starting page (if less than 1, it will be set to 1).
        :param end_page: Ending page (if None or greater than total, it will be set to the last page).
        :param custom_context: Custom text to insert in the prompt, enclosed in <custom_context> tags.
        :return: Resulting Markdown text.
        """
        pdf_data = self._download_pdf()
        reader = PdfReader(BytesIO(pdf_data))
        total_pages = len(reader.pages)

        # Adjust page range
        if start_page < 1:
            start_page = 1
        if end_page is None or end_page > total_pages:
            end_page = total_pages
        if start_page > end_page:
            raise ValueError("Invalid page range.")

        # If enabled, execute context auto-generation
        auto_context = ""
        total_auto_cost = 0
        total_auto_time = 0
        if self.auto_generate_context:
            all_text = ""
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text() or ""
                all_text += f"<START PAGE {page_num}>\n{page_text}\n<END PAGE {page_num}>\n\n"
            auto_context, auto_cost, auto_time = await self._auto_generate_context(all_text)
            self._auto_context = auto_context  # Store the auto-generated context
            total_auto_cost += auto_cost
            total_auto_time += auto_time

        # Load base prompt template
        base_prompt = self._load_prompt_template()

        # Create final prompt by combining contexts
        final_prompt = ""
        if auto_context:
            final_prompt += f"<custom_context>{auto_context}</custom_context>\n\n"
        if custom_context:
            final_prompt += f"<custom_context>{custom_context}</custom_context>\n\n"
        final_prompt += base_prompt + "\n\n"

        # Process pages (in parallel)
        tasks = []
        if self.show_progress:
            with tqdm(total=end_page - start_page + 1, desc="Processing pages") as pbar:
                async def process_page_with_progress(page_num):
                    result = await self._process_page(reader, page_num, final_prompt)
                    pbar.update(1)
                    return result

                tasks = [process_page_with_progress(page_num) for page_num in range(start_page, end_page + 1)]
                results = await asyncio.gather(*tasks)
        else:
            tasks = [self._process_page(reader, page_num, final_prompt) for page_num in range(start_page, end_page + 1)]
            results = await asyncio.gather(*tasks)

        markdown_pages = []
        total_page_cost = 0
        for page_text, page_cost in results:
            markdown_pages.append(page_text)
            total_page_cost += page_cost

        full_markdown = "\n\n".join(markdown_pages)

        if self.show_cost:
            total_cost = total_auto_cost + total_page_cost
            pages_cost = (end_page - start_page + 1) * 0.00017  # $0.00017 per page
            self.logger.info(f"Total conversion cost: {total_cost}")
            self.logger.info(f"Cost per page ($0.00017/page): ${pages_cost:.5f} for {end_page - start_page + 1} pages")

        # Output handling: if set to local or Azure, save file; otherwise return string
        if self.output_mode == "local" and self.output_path:
            # Ensure output directory exists before saving
            self._ensure_directory_exists(self.output_path)
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(full_markdown)
            self.logger.info(f"Markdown saved to {self.output_path}")
        elif self.output_mode == "azure":
            self._upload_output_to_azure(full_markdown)

        return full_markdown

    def get_auto_context(self) -> Optional[str]:
        """
        Get the auto-generated context if available.
        
        Returns:
            Optional[str]: The auto-generated context if it exists, None otherwise.
        """
        return self._auto_context