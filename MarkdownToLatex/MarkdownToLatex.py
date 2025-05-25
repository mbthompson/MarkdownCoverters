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
import shutil
import subprocess
import datetime

def get_unique_filename(basename):
    """
    Generate a filename that does not overwrite existing files.
    E.g., for basename '20250525.tex', returns '20250525.tex' or '20250525-1.tex', etc.
    """
    base, ext = os.path.splitext(basename)
    if ext == '':
        ext = '.tex'
    filename = base + ext
    index = 1
    while os.path.exists(filename):
        filename = f"{base}-{index}{ext}"
        index += 1
    return filename

def main():
    # Ensure pandoc is available
    if shutil.which('pandoc') is None:
        sys.exit("Error: pandoc not found. Please install pandoc and retry.")

    # Prompt user for Markdown input
    prompt = (
        "Enter/paste your Markdown text.\n"
        "Finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows):\n"
    )
    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        markdown_text = sys.stdin.read()
    except KeyboardInterrupt:
        sys.exit("\nInput cancelled. Exiting.")
    if not markdown_text.strip():
        sys.exit("No input received. Exiting.")

    # Determine output TEX filename
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_tex = f'{today_str}.tex'
    output_tex = get_unique_filename(default_tex)

    # Convert Markdown to LaTeX via Pandoc (read from stdin to avoid temp-file permission issues)
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
    else:
        print(f"LaTeX created: {output_tex}")
        # Attempt to compile the generated .tex to PDF
        pdf_file = os.path.splitext(output_tex)[0] + ".pdf"
        if shutil.which('pdflatex') is not None:
            try:
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', output_tex],
                    check=True,
                    env=env
                )
            except subprocess.CalledProcessError as e:
                sys.exit(f"Error: pdflatex failed with exit code {e.returncode}.")
            else:
                print(f"PDF created: {pdf_file}")
        else:
            print("Warning: pdflatex not found; skipping PDF compilation.")

if __name__ == '__main__':
    main()