# Legacy Individual Converters

This folder contains the original individual Markdown conversion tools. These have been moved here to keep the main directory clean while preserving their functionality.

## Available Tools

- **MarkdownToPDF/** - Converts Markdown to PDF with 1-inch margins
- **MarkdownToWord/** - Converts Markdown to Word (DOCX) format
- **MarkdownToLatex/** - Converts Markdown to LaTeX with PDF compilation

## When to Use These

- **Scripting and automation** - When you need to convert to a specific format programmatically
- **Single format workflows** - When you only work with one output format
- **Custom integrations** - When building tools that need format-specific converters

## Recommendation

For interactive use, we recommend the unified `MarkdownConverter.py` in the root directory, which provides a better user experience with an interactive menu system.

## Usage

Each tool works the same as before:

```bash
cd legacy/MarkdownToPDF
./MarkdownToPDF.py

cd legacy/MarkdownToWord  
./MarkdownToWord.py

cd legacy/MarkdownToLatex
./MarkdownToLatex.py
```

See the individual README files in each subdirectory for detailed usage instructions.