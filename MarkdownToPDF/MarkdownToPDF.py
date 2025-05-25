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
import shutil
import subprocess
import datetime

def get_unique_filename(basename):
    """
    Generate a filename that does not overwrite existing files.
    E.g., for basename 'output.pdf', returns 'output.pdf' or 'output-1.pdf', etc.
    """
    base, ext = os.path.splitext(basename)
    if ext == '':
        ext = '.pdf'
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

    # Ensure output directory exists
    output_dir = 'PDF'
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output PDF filename
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_pdf = os.path.join(output_dir, f'{today_str}.pdf')
    output_pdf = get_unique_filename(default_pdf)

    # Convert Markdown to PDF via Pandoc (read from stdin to avoid temp-file permission issues)
    try:
        # Override TMPDIR so Pandoc writes temp files in current directory
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
    else:
        print(f"PDF created: {output_pdf}")

if __name__ == '__main__':
    main()