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
 
 ## Individual Tools
 
 Each tool lives in its own subdirectory with detailed instructions:
 
 - **MarkdownToPDF/**
   - Converts Markdown to PDF with 1-inch margins.
   - Uses `pandoc -t pdf` under the hood.
   - See `MarkdownToPDF/README.md` for installation and usage.
 
 - **MarkdownToWord/**
   - Converts Markdown to Word (`.docx`).
   - Uses `pandoc -t docx`.
   - See `MarkdownToWord/README.md` for installation and usage.
 
 - **MarkdownToLatex/**
   - Converts Markdown to LaTeX (`.tex`) and compiles to PDF with 1-inch margins.
   - Uses `pandoc -t latex` and `pdflatex`.
   - See `MarkdownToLatex/README.md` for installation and usage.
 
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