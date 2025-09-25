#!/usr/bin/env python3
"""
MarkdownConverter - Unified Markdown Conversion Tool

A single interface for converting Markdown to PDF, Word (DOCX), or LaTeX.
Choose your output format interactively and paste your Markdown content.
Requires Pandoc to be installed and on your PATH.
For LaTeX output, also requires pdflatex.
"""
import sys
import os
import subprocess
from markdown_utils import (
    get_unique_filename, check_pandoc, check_pdflatex, 
    get_markdown_input, ensure_output_dir, get_dated_filename, 
    run_pandoc, run_pdflatex, save_markdown_file,
    load_config, build_pandoc_args, open_file
)

def check_dependencies():
    """Check if required dependencies are available."""
    check_pandoc()
    return check_pdflatex()

def get_user_choice():
    """Display menu and get user's choice for output format."""
    print("=" * 60)
    print("📄 Markdown Conversion Tool")
    print("=" * 60)
    print("Choose your output format:")
    print("  1. PDF")
    print("  2. Word (DOCX)")
    print("  3. LaTeX (with PDF compilation)")
    print("  4. Exit")
    print("-" * 60)
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

def get_markdown_input_with_prompt():
    """Get Markdown text from user input with custom prompt."""
    prompt = (
        "\nEnter/paste your Markdown text.\n"
        "Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):\n"
        + "-" * 60 + "\n"
    )

    return get_markdown_input(prompt)

def convert_to_pdf(markdown_text, config=None, slug=None):
    """Convert Markdown to PDF."""
    if config is None:
        config = load_config()
    
    output_dir = 'PDF'
    ensure_output_dir(output_dir)
    output_pdf = get_dated_filename(output_dir, 'pdf', markdown_text, slug)
    
    # Build pandoc arguments with configuration
    base_args = ['pandoc', '-f', 'markdown', '-o', output_pdf]
    pandoc_args = build_pandoc_args(base_args, config['pdf'])

    success = run_pandoc(pandoc_args, markdown_text)
    if not success:
        print(f"⚠️  Warning: pandoc reported errors while generating {output_pdf}.")

    # Save the markdown source file if configured
    if config['global']['save_markdown_source']:
        md_file = save_markdown_file(markdown_text, output_pdf)
        if md_file:
            print(f"📝 Markdown saved: {md_file}")

    if config['global'].get('auto_open_output') and os.path.exists(output_pdf):
        open_file(output_pdf)

    return output_pdf

def convert_to_word(markdown_text, config=None, slug=None):
    """Convert Markdown to Word (DOCX)."""
    if config is None:
        config = load_config()
    
    output_dir = 'DOCX'
    ensure_output_dir(output_dir)
    output_docx = get_dated_filename(output_dir, 'docx', markdown_text, slug)
    
    # Build pandoc arguments with configuration
    base_args = ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_docx]
    pandoc_args = build_pandoc_args(base_args, config['docx'])

    success = run_pandoc(pandoc_args, markdown_text)
    if not success:
        print(f"⚠️  Warning: pandoc reported errors while generating {output_docx}.")

    # Save the markdown source file if configured
    if config['global']['save_markdown_source']:
        md_file = save_markdown_file(markdown_text, output_docx)
        if md_file:
            print(f"📝 Markdown saved: {md_file}")

    if config['global'].get('auto_open_output') and os.path.exists(output_docx):
        open_file(output_docx)

    return output_docx

def convert_to_latex(markdown_text, has_pdflatex, config=None, slug=None):
    """Convert Markdown to LaTeX and optionally compile to PDF."""
    if config is None:
        config = load_config()
    
    output_dir = 'LaTeX'
    ensure_output_dir(output_dir)
    output_tex = get_dated_filename(output_dir, 'tex', markdown_text, slug)
    
    # Build pandoc arguments with configuration
    base_args = ['pandoc', '-s', '-f', 'markdown', '-t', 'latex', '-o', output_tex]
    pandoc_args = build_pandoc_args(base_args, config['latex'])

    success = run_pandoc(pandoc_args, markdown_text)
    if not success:
        print(f"⚠️  Warning: pandoc reported errors while generating {output_tex}.")

    if os.path.exists(output_tex):
        print(f"✅ LaTeX created: {output_tex}")
    else:
        print(f"❌ Failed to create LaTeX file: {output_tex}")
        return output_tex, None
    
    # Save the markdown source file if configured
    if config['global']['save_markdown_source']:
        md_file = save_markdown_file(markdown_text, output_tex)
        if md_file:
            print(f"📝 Markdown saved: {md_file}")
    
    # Check if PDF compilation should be attempted (config setting and pdflatex availability)
    should_compile = config['latex'].get('compile_pdf', True) and has_pdflatex
    
    if should_compile and os.path.exists(output_tex):
        success, pdf_file = run_pdflatex(output_tex, output_dir)
        if success:
            print(f"✅ PDF created: {pdf_file}")
            if config['global'].get('auto_open_output') and os.path.exists(pdf_file):
                open_file(pdf_file)
            return output_tex, pdf_file
        else:
            print(f"⚠️  Warning: pdflatex failed.")
            print(f"LaTeX file created successfully: {output_tex}")
            if config['global'].get('auto_open_output') and os.path.exists(output_tex):
                open_file(output_tex)
            return output_tex, None
    elif not has_pdflatex:
        print("⚠️  Warning: pdflatex not found; skipping PDF compilation.")
        print(f"LaTeX file created successfully: {output_tex}")
        if config['global'].get('auto_open_output') and os.path.exists(output_tex):
            open_file(output_tex)
        return output_tex, None
    else:
        print("ℹ️  PDF compilation disabled in configuration.")
        print(f"LaTeX file created successfully: {output_tex}")
        if config['global'].get('auto_open_output') and os.path.exists(output_tex):
            open_file(output_tex)
        return output_tex, None

def main():
    """Main program flow."""
    # Check dependencies and load configuration
    has_pdflatex = check_dependencies()
    config = load_config()
    
    while True:
        choice = get_user_choice()
        
        if choice == '4':
            print("👋 Goodbye!")
            sys.exit(0)
        
        # Ask for optional file name to append after the date
        slug_input = input(
            "Enter a name to include in the output filename (optional): "
        ).strip()
        slug = slug_input if slug_input else None

        # Get markdown input
        markdown_text = get_markdown_input_with_prompt()
        
        print("\n🔄 Converting...")
        
        try:
            if choice == '1':
                output_file = convert_to_pdf(markdown_text, config, slug)
                print(f"✅ PDF created: {output_file}")
            
            elif choice == '2':
                output_file = convert_to_word(markdown_text, config, slug)
                print(f"✅ DOCX created: {output_file}")
            
            elif choice == '3':
                if not has_pdflatex and config['latex'].get('compile_pdf', True):
                    print("⚠️  Note: pdflatex not found. Only LaTeX file will be generated.")
                tex_file, pdf_file = convert_to_latex(markdown_text, has_pdflatex, config, slug)
                # Success messages are printed within the function
            
            print("\n" + "=" * 60)
            another = input("Convert another file? (y/N): ").strip().lower()
            if another not in ['y', 'yes']:
                print("👋 Goodbye!")
                break
            print()  # Add blank line for readability
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n" + "=" * 60)
            retry = input("Try again? (y/N): ").strip().lower()
            if retry not in ['y', 'yes']:
                print("👋 Goodbye!")
                break
            print()  # Add blank line for readability

if __name__ == '__main__':
    main()
