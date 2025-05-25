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
    run_pandoc, run_pdflatex, save_markdown_file
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
    print("\nEnter/paste your Markdown text.")
    print("Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):")
    print("-" * 60)
    
    return get_markdown_input()

def convert_to_pdf(markdown_text):
    """Convert Markdown to PDF."""
    output_dir = 'PDF'
    ensure_output_dir(output_dir)
    output_pdf = get_dated_filename(output_dir, 'pdf')
    
    run_pandoc(
        ['pandoc', '-f', 'markdown', '-V', 'geometry:margin=1in', '-o', output_pdf],
        markdown_text
    )
    
    # Save the markdown source file
    md_file = save_markdown_file(markdown_text, output_pdf)
    if md_file:
        print(f"📝 Markdown saved: {md_file}")
    
    return output_pdf

def convert_to_word(markdown_text):
    """Convert Markdown to Word (DOCX)."""
    output_dir = 'DOCX'
    ensure_output_dir(output_dir)
    output_docx = get_dated_filename(output_dir, 'docx')
    
    run_pandoc(
        ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_docx],
        markdown_text
    )
    
    # Save the markdown source file
    md_file = save_markdown_file(markdown_text, output_docx)
    if md_file:
        print(f"📝 Markdown saved: {md_file}")
    
    return output_docx

def convert_to_latex(markdown_text, has_pdflatex):
    """Convert Markdown to LaTeX and optionally compile to PDF."""
    output_dir = 'LaTeX'
    ensure_output_dir(output_dir)
    output_tex = get_dated_filename(output_dir, 'tex')
    
    run_pandoc(
        ['pandoc', '-s', '-f', 'markdown', '-t', 'latex', '-V', 'geometry:margin=1in', '-o', output_tex],
        markdown_text
    )
    
    print(f"✅ LaTeX created: {output_tex}")
    
    # Save the markdown source file
    md_file = save_markdown_file(markdown_text, output_tex)
    if md_file:
        print(f"📝 Markdown saved: {md_file}")
    
    # Attempt to compile the generated .tex to PDF
    if has_pdflatex:
        success, pdf_file = run_pdflatex(output_tex, output_dir)
        if success:
            print(f"✅ PDF created: {pdf_file}")
            return output_tex, pdf_file
        else:
            print(f"⚠️  Warning: pdflatex failed.")
            print(f"LaTeX file created successfully: {output_tex}")
            return output_tex, None
    else:
        print("⚠️  Warning: pdflatex not found; skipping PDF compilation.")
        print(f"LaTeX file created successfully: {output_tex}")
        return output_tex, None

def main():
    """Main program flow."""
    # Check dependencies
    has_pdflatex = check_dependencies()
    
    while True:
        choice = get_user_choice()
        
        if choice == '4':
            print("👋 Goodbye!")
            sys.exit(0)
        
        # Get markdown input
        markdown_text = get_markdown_input_with_prompt()
        
        print("\n🔄 Converting...")
        
        try:
            if choice == '1':
                output_file = convert_to_pdf(markdown_text)
                print(f"✅ PDF created: {output_file}")
            
            elif choice == '2':
                output_file = convert_to_word(markdown_text)
                print(f"✅ DOCX created: {output_file}")
            
            elif choice == '3':
                if not has_pdflatex:
                    print("⚠️  Note: pdflatex not found. Only LaTeX file will be generated.")
                tex_file, pdf_file = convert_to_latex(markdown_text, has_pdflatex)
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