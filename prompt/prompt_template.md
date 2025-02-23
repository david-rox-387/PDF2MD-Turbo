
<instructions>  
Faithfully convert the PDF page into a Markdown document, preserving the original order, structure, and formatting. Ensure that each element is accurately transcribed using the appropriate Markdown format for a complete and precise conversion.  
</instructions>  

<rules>  
1. **Headings:**  
   - Use the `#` symbol for headings, maintaining the original hierarchy (e.g., `#` for the main title, `##` for subtitles, etc.).  
2. **Lists:**  
   - Use `*` for unordered lists.  
   - Use `1.`, `2.`, etc., for ordered lists.  
3. **Text Formatting:**  
   - Use **bold** to highlight important parts.  
   - Use *italic* to emphasize specific words or phrases.  
4. **Tables:** Convert all tables into Markdown format using the following structure:  

   
   | Header 1     | Header 2     |
   |-------------|-------------|
   | Data 1      | Data 2      |
   

5. **Images:**  
   - If available, use the Markdown syntax for images: `![Description](Optional-URL)`.  
   - If the URL is unavailable, provide a detailed description of the visual content, including colors, shapes, placements, and any visible text.  
6. **Charts and Diagrams:**  
   - Provide a complete description of the data, highlighting trends, relationships, and key points.  
   - Include any visual annotations that aid in understanding.  
7. **Mathematical Formulas:**  
   - Convert all formulas into LaTeX.  
   - For inline formulas, enclose them within `$` (e.g., `$a^2+b^2=c^2$`).  
   - For block formulas, use `$$` (e.g., `$$E=mc^2$$`).  
8. **Structure and Content:**  
   - Maintain the original order and formatting.  
   - Do not include page numbers, footers, or annotations that are not part of the main content.  
</rules>  

<output>  
Return only the document in Markdown format, without adding explanations, comments, or supplementary information.  
The output **must strictly adhere to the original language of the text** without translation. 
</output>  

<IMPORTANT>  
- Do not include page numbers, footers, or other annotations that are not part of the main content.  
- Since you are analyzing the content of a single PDF page within a larger document, consider that the text may be truncated or incomplete. When encountering an unfinished sentence, do not generate additional text; leave it as is, as it might continue on the next processed page.  
- The same applies to truncated tables, images, formulas, and footnotes—do not attempt to complete or infer missing content.  
- When writing Markdown, **DO NOT** use triple backticks (` ``` `) to open and close the Markdown content—just write the Markdown directly.  
</IMPORTANT>  