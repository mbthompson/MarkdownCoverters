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
    get_dated_filename, run_pandoc, run_pdflatex, save_markdown_file,
    load_config, build_pandoc_args, open_file
)

def main():
    # Ensure pandoc is available and load configuration
    check_pandoc()
    config = load_config()

    # Get Markdown input from user
    markdown_text = get_markdown_input()

    # Setup output
    output_dir = 'LaTeX'
    ensure_output_dir(output_dir)
    output_tex = get_dated_filename(output_dir, 'tex')

    # Build pandoc arguments with configuration
    base_args = ['pandoc', '-s', '-f', 'markdown', '-t', 'latex', '-o', output_tex]
    pandoc_args = build_pandoc_args(base_args, config['latex'])
    
    # Convert Markdown to LaTeX via Pandoc
    run_pandoc(pandoc_args, markdown_text)
    
    # Save the markdown source file if configured
    if config['global']['save_markdown_source']:
        md_file = save_markdown_file(markdown_text, output_tex)
        if md_file:
            print(f"Markdown saved: {md_file}")
    
    print(f"LaTeX created: {output_tex}")

    # Check if PDF compilation should be attempted
    has_pdflatex = check_pdflatex()
    should_compile = config['latex'].get('compile_pdf', True) and has_pdflatex
    
    if should_compile:
        success, pdf_file = run_pdflatex(output_tex, output_dir)
        if success:
            print(f"PDF created: {pdf_file}")
            if config['global'].get('auto_open_output'):
                open_file(pdf_file)
        else:
            if config['global'].get('auto_open_output'):
                open_file(output_tex)
            sys.exit(f"Error: pdflatex failed.")
    elif not has_pdflatex:
        print("Warning: pdflatex not found; skipping PDF compilation.")
        if config['global'].get('auto_open_output'):
            open_file(output_tex)
    else:
        print("Info: PDF compilation disabled in configuration.")
        if config['global'].get('auto_open_output'):
            open_file(output_tex)

if __name__ == '__main__':
    main()