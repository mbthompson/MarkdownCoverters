# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a Markdown Conversion Toolkit containing three standalone CLI Python tools:

- **MarkdownToPDF/**: Converts Markdown to PDF with 1-inch margins (uses `pandoc -t pdf`)
- **MarkdownToWord/**: Converts Markdown to Word DOCX format (uses `pandoc -t docx`) 
- **MarkdownToLatex/**: Converts Markdown to LaTeX and compiles to PDF (uses `pandoc -t latex` + `pdflatex`)

Each tool directory contains:
- Python script (e.g., `MarkdownToPDF.py`)
- macOS .app launcher bundle for Terminal integration
- AppleScript source file (.scpt) for the launcher
- Individual README.md with usage instructions

## Architecture

All three tools follow the same pattern:
- Read Markdown from stdin (interactive mode or piped input)
- Use Pandoc subprocess calls for conversion
- Generate unique output filenames to avoid overwrites
- Set TMPDIR to current directory for Pandoc temp files
- Handle errors gracefully with informative messages

Key shared functions:
- `get_unique_filename()`: Prevents file overwrites by appending incrementing numbers
- All tools require Pandoc on PATH; LaTeX tool additionally requires pdflatex

## Common Commands

### Make scripts executable:
```bash
chmod +x MarkdownToPDF/MarkdownToPDF.py
chmod +x MarkdownToWord/MarkdownToWord.py  
chmod +x MarkdownToLatex/MarkdownToLatex.py
```

### Test tools:
```bash
# Interactive mode
./MarkdownToPDF/MarkdownToPDF.py

# File mode
cat mydoc.md | ./MarkdownToWord/MarkdownToWord.py
```

### Prerequisites check:
- Pandoc: `pandoc --version`
- LaTeX (for MarkdownToLatex): `pdflatex --version`

## Development Notes

- No external Python dependencies beyond standard library
- All tools use subprocess to call external commands (pandoc, pdflatex)
- Output files use date-based naming (PDF) or generic naming with increment suffixes
- Each tool works independently - no shared code modules
- macOS .app bundles use AppleScript to launch Terminal and run Python scripts