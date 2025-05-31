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
    get_dated_filename, run_pandoc, save_markdown_file,
    load_config, build_pandoc_args
)

def main():
    # Ensure pandoc is available and load configuration
    check_pandoc()
    config = load_config()

    # Get Markdown input from user
    markdown_text = get_markdown_input()

    # Setup output
    output_dir = 'DOCX'
    ensure_output_dir(output_dir)
    output_docx = get_dated_filename(output_dir, 'docx')

    # Build pandoc arguments with configuration
    base_args = ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_docx]
    pandoc_args = build_pandoc_args(base_args, config['docx'])
    
    # Convert Markdown to DOCX via Pandoc
    run_pandoc(pandoc_args, markdown_text)
    
    # Save the markdown source file if configured
    if config['global']['save_markdown_source']:
        md_file = save_markdown_file(markdown_text, output_docx)
        if md_file:
            print(f"Markdown saved: {md_file}")
    
    print(f"DOCX created: {output_docx}")

if __name__ == '__main__':
    main()