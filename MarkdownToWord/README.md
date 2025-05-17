# MarkdownToWord

CLI tool to convert Markdown to Word (DOCX) via Pandoc.

**MarkdownToWord** reads Markdown from stdin (interactive or piped) and outputs a DOCX using Pandoc.

## Prerequisites

- Python 3
- Pandoc (https://pandoc.org/) installed and available on your PATH.

## Installation

Clone the repository or download the script, then make it executable:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/MarkdownToWord
chmod +x MarkdownToWord.py
```

## Usage

### Interactive Mode

Paste or type your Markdown into stdin, then end the input with EOF:

```bash
./MarkdownToWord.py
```

Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows).

### File Mode

Pipe a Markdown file directly:

```bash
cat mydoc.md | ./MarkdownToWord.py
```

Generated files: `output.docx` (or `output-1.docx`, etc.).

## Example

```bash
$ ./MarkdownToWord.py
Enter/paste your Markdown text.
Finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows):
# Hello World

This is *Markdown*.
[Ctrl-D]
DOCX created: output.docx
```