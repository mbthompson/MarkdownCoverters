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
import shutil
import subprocess
import datetime

def get_unique_filename(basename):
    """
    Generate a filename that does not overwrite existing files.
    E.g., for basename 'PDF/20250525.pdf', returns 'PDF/20250525.pdf' or 'PDF/20250525-1.pdf', etc.
    """
    base, ext = os.path.splitext(basename)
    filename = basename
    index = 1
    while os.path.exists(filename):
        filename = f"{base}-{index}{ext}"
        index += 1
    return filename

def check_dependencies():
    """Check if required dependencies are available."""
    if shutil.which('pandoc') is None:
        sys.exit("Error: pandoc not found. Please install pandoc and retry.")
    
    # Check for pdflatex (only needed for LaTeX, but good to know)
    has_pdflatex = shutil.which('pdflatex') is not None
    return has_pdflatex

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

def get_markdown_input():
    """Get Markdown text from user input."""
    print("\nEnter/paste your Markdown text.")
    print("Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):")
    print("-" * 60)
    
    try:
        markdown_text = sys.stdin.read()
    except KeyboardInterrupt:
        sys.exit("\nInput cancelled. Exiting.")
    
    if not markdown_text.strip():
        sys.exit("No input received. Exiting.")
    
    return markdown_text

def convert_to_pdf(markdown_text):
    """Convert Markdown to PDF."""
    # Ensure output directory exists
    output_dir = 'PDF'
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output PDF filename
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_pdf = os.path.join(output_dir, f'{today_str}.pdf')
    output_pdf = get_unique_filename(default_pdf)
    
    # Convert Markdown to PDF via Pandoc
    try:
        env = os.environ.copy()
        env['TMPDIR'] = os.getcwd()
        subprocess.run(
            ['pandoc', '-f', 'markdown', '-V', 'geometry:margin=1in', '-o', output_pdf],
            input=markdown_text.encode('utf-8'),
            check=True,
            env=env
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc failed with exit code {e.returncode}.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")
    
    return output_pdf

def convert_to_word(markdown_text):
    """Convert Markdown to Word (DOCX)."""
    # Ensure output directory exists
    output_dir = 'DOCX'
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output DOCX filename
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_docx = os.path.join(output_dir, f'{today_str}.docx')
    output_docx = get_unique_filename(default_docx)
    
    # Convert Markdown to DOCX via Pandoc
    try:
        env = os.environ.copy()
        env['TMPDIR'] = os.getcwd()
        subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'docx', '-o', output_docx],
            input=markdown_text.encode('utf-8'),
            check=True,
            env=env
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc failed with exit code {e.returncode}.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")
    
    return output_docx

def convert_to_latex(markdown_text, has_pdflatex):
    """Convert Markdown to LaTeX and optionally compile to PDF."""
    # Ensure output directory exists
    output_dir = 'LaTeX'
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output TEX filename
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_tex = os.path.join(output_dir, f'{today_str}.tex')
    output_tex = get_unique_filename(default_tex)
    
    # Convert Markdown to LaTeX via Pandoc
    try:
        env = os.environ.copy()
        env['TMPDIR'] = os.getcwd()
        subprocess.run(
            ['pandoc', '-s', '-f', 'markdown', '-t', 'latex', '-V', 'geometry:margin=1in', '-o', output_tex],
            input=markdown_text.encode('utf-8'),
            check=True,
            env=env
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc failed with exit code {e.returncode}.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")
    
    print(f"✅ LaTeX created: {output_tex}")
    
    # Attempt to compile the generated .tex to PDF
    if has_pdflatex:
        pdf_file = os.path.splitext(output_tex)[0] + ".pdf"
        try:
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', output_tex],
                check=True,
                env=env
            )
            print(f"✅ PDF created: {pdf_file}")
            return output_tex, pdf_file
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: pdflatex failed with exit code {e.returncode}.")
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
        markdown_text = get_markdown_input()
        
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