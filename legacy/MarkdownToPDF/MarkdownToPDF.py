#!/usr/bin/env python3
"""
MarkdownToPDF

Terminal-based Markdown to PDF converter.
Paste or type your Markdown input, finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows),
and the script will generate a PDF in the current directory without overwriting existing files.
Requires Pandoc to be installed and on your PATH.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from markdown_utils import (
    check_pandoc, get_markdown_input, ensure_output_dir, 
    get_dated_filename, run_pandoc
)

def main():
    # Ensure pandoc is available
    check_pandoc()

    # Get Markdown input from user
    markdown_text = get_markdown_input()

    # Setup output
    output_dir = 'PDF'
    ensure_output_dir(output_dir)
    output_pdf = get_dated_filename(output_dir, 'pdf')

    # Convert Markdown to PDF via Pandoc
    run_pandoc(
        ['pandoc', '-f', 'markdown', '-V', 'geometry:margin=1in', '-o', output_pdf],
        markdown_text
    )
    
    print(f"PDF created: {output_pdf}")

if __name__ == '__main__':
    main()