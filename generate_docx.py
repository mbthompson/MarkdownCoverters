#!/usr/bin/env python3
"""
generate_docx.py

Creates a sample .docx file with headings and sample text.
"""
import sys

try:
    from docx import Document
except ImportError:
    sys.exit("Error: python-docx package is required. Install with 'pip install python-docx'.")

def main():
    doc = Document()
    doc.add_heading('Heading 1', level=1)
    doc.add_heading('Heading 2', level=2)
    doc.add_paragraph('This is a sample paragraph under Heading 2.')
    doc.add_paragraph('Another paragraph of sample text.')
    output_filename = 'sample.docx'
    doc.save(output_filename)
    print(f'Created {output_filename}')

if __name__ == '__main__':  # noqa: E402
    main()