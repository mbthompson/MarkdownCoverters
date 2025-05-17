# MarkdownToPDF

CLI tool to convert Markdown to PDF with 1-inch margins via Pandoc.

**MarkdownToPDF** reads Markdown from stdin (interactive or piped) and outputs a PDF using Pandoc.
Generated PDFs use a default 1-inch margin.

Prerequisites
-------------
- Python 3
- Pandoc (https://pandoc.org/) installed and available on your PATH.

Installation
------------
No installation is required beyond having Pandoc and Python 3. Just make the script executable:

    cd MarkdownToPDF
    chmod +x MarkdownToPDF.py

Usage
-----
Run the converter, then paste or type your Markdown. Finish with an EOF (Ctrl-D on Unix/macOS, Ctrl-Z then Enter on Windows).

    ./MarkdownToPDF.py

Step-by-step:
1. In Terminal, navigate to this folder:
       cd MarkdownToPDF
2. Make the script executable (if you haven’t already):
       chmod +x MarkdownToPDF.py
3. Launch it:
       ./MarkdownToPDF.py
4. Paste or type your Markdown text.
5. Press Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows) to finish input.
6. The script writes output.pdf (or output-1.pdf, etc., if it already exists) in the current directory.

Example session:
    $ ./MarkdownToPDF.py
    Enter/paste your Markdown text.
    Finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows):
    # Hello World

    This is *Markdown*.
    [Ctrl-D]
PDF created: output.pdf

## macOS Launcher

This directory includes a bundled macOS application and its AppleScript source to simplify launching:

- **MarkdownToPDF.app**: Double-click this app to open Terminal and automatically run `MarkdownToPDF.py`.
- **MarkdownToPDF.scpt**: The AppleScript source for the launcher. Open and edit this in Script Editor to customize the launch command.