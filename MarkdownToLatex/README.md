# MarkdownToLatex

CLI tool to convert Markdown to LaTeX (.tex) and PDF with 1-inch margins via Pandoc.

**MarkdownToLatex** reads Markdown from stdin (interactive or piped) and outputs a LaTeX file + PDF using Pandoc.
Generated files include the geometry package with a default 1″ margin.

## Prerequisites

- Python 3
- Pandoc (https://pandoc.org/) installed and available on your PATH.
- A LaTeX engine (e.g., pdflatex) installed and available on your PATH.

## Installation

Clone the repository or download the script, then make it executable:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/MarkdownToLatex
chmod +x MarkdownToLatex.py
```

## Usage


### Interactive Mode

Paste or type your Markdown into stdin, then end the input with EOF:

```bash
./MarkdownToLatex.py
```

Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows).

After conversion, you will have both `output.tex` and `output.pdf` in the current directory.

### File Mode

Pipe a Markdown file directly, then compile to PDF:

```bash
cat mydoc.md | ./MarkdownToLatex.py
```

Generated files: `output.tex` (or `output-1.tex`, etc.) and corresponding PDF.

## Example

```bash
$ ./MarkdownToLatex.py
Enter/paste your Markdown text.
Finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows):
# Hello World

This is *Markdown*.
[Ctrl-D]
LaTeX created: output.tex
PDF created: output.pdf
```