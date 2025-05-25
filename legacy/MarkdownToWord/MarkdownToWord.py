#!/usr/bin/env python3
"""
MarkdownToWord

Terminal-based Markdown to Word (DOCX) converter.
Paste or type your Markdown input, finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows),
and the script will generate a DOCX file in the current directory without overwriting existing files.
Requires Pandoc to be installed and on your PATH.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from markdown_utils import (
    check_pandoc, get_markdown_input, ensure_output_dir, 
    get_dated_filename, run_pandoc, save_markdown_file
)

def main():
    # Ensure pandoc is available
    check_pandoc()

    # Get Markdown input from user
    markdown_text = get_markdown_input()

    # Setup output
    output_dir = 'DOCX'
    ensure_output_dir(output_dir)
    output_docx = get_dated_filename(output_dir, 'docx')

    # Convert Markdown to DOCX via Pandoc
    run_pandoc(
        ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_docx],
        markdown_text
    )
    
    # Save the markdown source file
    md_file = save_markdown_file(markdown_text, output_docx)
    
    print(f"DOCX created: {output_docx}")
    if md_file:
        print(f"Markdown saved: {md_file}")

if __name__ == '__main__':
    main()