#!/usr/bin/env python3
"""
MarkdownToLatex

Terminal-based Markdown to LaTeX (and PDF) converter.
Paste or type your Markdown input, finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows),
and the script will generate a LaTeX (.tex) file (and compile to PDF) in the current directory without overwriting existing files.
Requires Pandoc and pdflatex to be installed and on your PATH.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from markdown_utils import (
    check_pandoc, check_pdflatex, get_markdown_input, ensure_output_dir, 
    get_dated_filename, run_pandoc, run_pdflatex, save_markdown_file
)

def main():
    # Ensure pandoc is available
    check_pandoc()

    # Get Markdown input from user
    markdown_text = get_markdown_input()

    # Setup output
    output_dir = 'LaTeX'
    ensure_output_dir(output_dir)
    output_tex = get_dated_filename(output_dir, 'tex')

    # Convert Markdown to LaTeX via Pandoc
    run_pandoc(
        ['pandoc', '-s', '-f', 'markdown', '-t', 'latex', '-V', 'geometry:margin=1in', '-o', output_tex],
        markdown_text
    )
    
    # Save the markdown source file
    md_file = save_markdown_file(markdown_text, output_tex)
    
    print(f"LaTeX created: {output_tex}")
    if md_file:
        print(f"Markdown saved: {md_file}")
    
    # Attempt to compile the generated .tex to PDF
    if check_pdflatex():
        success, pdf_file = run_pdflatex(output_tex, output_dir)
        if success:
            print(f"PDF created: {pdf_file}")
        else:
            sys.exit(f"Error: pdflatex failed.")
    else:
        print("Warning: pdflatex not found; skipping PDF compilation.")

if __name__ == '__main__':
    main()