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

Generated files: Files in `DOCX/` folder named with current date (e.g. `DOCX/20250525.docx`, or `DOCX/20250525-1.docx`, etc.).

## Example

```bash
$ ./MarkdownToWord.py
Enter/paste your Markdown text.
Finish with Ctrl-D (Unix) or Ctrl-Z then Enter (Windows):
# Hello World

This is *Markdown*.
[Ctrl-D]
DOCX created: DOCX/20250525.docx
```
## macOS Launcher

This directory includes a bundled macOS application and its AppleScript source to simplify launching:

- **MarkdownToWord.app**: Double-click this app to open Terminal and automatically run `MarkdownToWord.py`.
- **MarkdownToWord.scpt**: The AppleScript source for the launcher. Open and edit this in Script Editor to customize the launch command.