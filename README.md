 # Markdown Conversion Toolkit
 
 This repository provides both a **unified interactive converter** and three standalone CLI tools for converting Markdown into common document formats using Pandoc (and pdflatex for LaTeX/PDF).
 
 ## 🆕 Unified Converter (Recommended)
 
 **MarkdownConverter.py** - A single interactive tool for all conversions:
 - Interactive menu to choose output format (PDF, Word, LaTeX)
 - Paste your Markdown and get instant conversion
 - Organized output folders with date-based naming
 - See `README_UNIFIED.md` for complete documentation
 
 ```bash
 ./MarkdownConverter.py
 ```

 **macOS Desktop Integration**: Double-click `MarkdownConverter.app` to open Terminal and automatically run the unified converter.
 
 ## Legacy Individual Tools
 
 The original individual tools are preserved in the `legacy/` folder for users who prefer single-format converters or need them for scripting:
 
 - **legacy/MarkdownToPDF/** - PDF-only converter
 - **legacy/MarkdownToWord/** - Word-only converter  
 - **legacy/MarkdownToLatex/** - LaTeX-only converter
 
 Each maintains its original functionality and documentation.
 
 ## Prerequisites
 
 - **Python 3**
 - **Pandoc**: https://pandoc.org/
 - **pdflatex** (for MarkdownToLatex) or any LaTeX engine available on your PATH
 
 ## Getting Started
 
 1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```
 2. Navigate into the tool directory you wish to use, make the script executable, and run it:
    ```bash
    cd MarkdownToPDF
    chmod +x MarkdownToPDF.py
    ./MarkdownToPDF.py
    ```
 
 For detailed options and examples, refer to each tool’s own README file.