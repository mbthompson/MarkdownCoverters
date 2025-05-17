#!/usr/bin/env python3
"""
generate_tex.py

Creates a sample LaTeX (.tex) file with sections and sample text using PyLaTeX.
"""
import sys

try:
    from pylatex import Document, Section, Subsection, Command
    from pylatex.utils import NoEscape
except ImportError:
    sys.exit("Error: pylatex package is required. Install with 'pip install pylatex'.")

def main():
    doc = Document('generated')  # base filename 'generated.tex'

    # Preamble: title, author, date
    doc.preamble.append(Command('title', 'Generated LaTeX Document'))
    doc.preamble.append(Command('author', 'Your Name'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r'\tableofcontents\newpage'))

    # Sections and subsections with sample text
    with doc.create(Section('Introduction')):
        doc.append('This is the introduction.')
    with doc.create(Section('Background')):
        doc.append('Background information goes here.')
        with doc.create(Subsection('History')):
            doc.append('Historical context and details.')
    with doc.create(Section('Methods')):
        doc.append('Describe your methodology here.')
    with doc.create(Section('Results')):
        doc.append('Results are presented in this section.')
    with doc.create(Section('Conclusion')):
        doc.append('Conclusions and future work.')

    # Save .tex file
    doc.generate_tex()
    print('Created generated.tex. Compile with: latexmk -pdf generated.tex')

if __name__ == '__main__':
    main()