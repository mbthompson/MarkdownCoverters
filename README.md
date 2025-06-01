# Markdown Conversion Toolkit

A streamlined toolkit for converting Markdown to PDF, Word (DOCX), and LaTeX formats. Features both a **unified interactive converter** and standalone CLI tools, all built on a **shared core module** for consistent behavior and maintainability.

## 🚀 Key Features

- **Unified interactive interface** for all conversion formats
- **Standalone legacy tools** for scripting and automation  
- **Shared core module** (`markdown_utils.py`) eliminates code duplication
- **Anti-overwrite protection** with automatic file naming
- **macOS desktop integration** via .app bundles
- **No external Python dependencies** - uses only standard library + pandoc/pdflatex
- **Auto-open**: Converted files open automatically after conversion. On macOS,
  PDFs open in Preview and DOCX in Microsoft Word. Set `"auto_open_output": false`
  to disable.

## 🆕 Unified Converter (Recommended)

**MarkdownConverter.py** - Interactive tool for all conversions:
- Interactive menu to choose output format (PDF, Word, LaTeX)
- Paste your Markdown and get instant conversion
 - Organized output folders with date plus snippet naming
- Built on shared `markdown_utils.py` module

```bash
./MarkdownConverter.py
```

**macOS Desktop Integration**: Double-click `MarkdownConverter.app` to open Terminal and run the converter.

## 🔧 Legacy Tools (for Scripting)

Individual tools in the `legacy/` folder maintain standalone operation while using shared core functionality:

- **legacy/MarkdownToPDF/** - PDF-only converter
- **legacy/MarkdownToWord/** - Word-only converter  
- **legacy/MarkdownToLatex/** - LaTeX-only converter

Perfect for automation, CI/CD pipelines, and shell scripts:
```bash
echo "# My Document" | ./legacy/MarkdownToPDF/MarkdownToPDF.py
```

## 🏗️ Architecture

### Shared Module (`markdown_utils.py`)
Core functionality used by all converters:
- **File management**: Anti-overwrite protection, directory creation
- **Process management**: Pandoc/pdflatex subprocess wrappers
- **Dependency checking**: Validates required tools
- **Input handling**: Consistent stdin processing

### Benefits of Refactored Architecture
- **70% code reduction** across all tools
- **Single source of truth** for core logic
- **Consistent behavior** between unified and legacy tools
- **Easier maintenance** and feature additions

## 📋 Prerequisites

- **Python 3** (standard library only)
- **Pandoc**: https://pandoc.org/ (required for all conversions)
- **pdflatex** (optional, for LaTeX PDF compilation)

## 🚀 Quick Start

### Unified Converter
```bash
# Clone and run
git clone <repository-url>
cd markdown-conversion-toolkit
chmod +x MarkdownConverter.py
./MarkdownConverter.py
```

### Legacy Tools for Scripting
```bash
# Make executable
chmod +x legacy/MarkdownToPDF/MarkdownToPDF.py
chmod +x legacy/MarkdownToWord/MarkdownToWord.py
chmod +x legacy/MarkdownToLatex/MarkdownToLatex.py

# Interactive mode
./legacy/MarkdownToPDF/MarkdownToPDF.py

# Pipe mode (great for scripts)
cat document.md | ./legacy/MarkdownToWord/MarkdownToWord.py
```

### Test Installation
```bash
# Verify shared module works
python3 -c "from markdown_utils import check_pandoc; check_pandoc(); print('✅ Setup complete!')"
```

## 📁 Output Organization

- All tools create organized output folders:
- **PDF/**: PDF files named with the date and first six words (e.g., `20250525HelloWorldThisIsMy.pdf`)
- **DOCX/**: Word documents
- **LaTeX/**: LaTeX source files and compiled PDFs

### Auto-Open Output

Output files open automatically after conversion. Set
`"auto_open_output": false` in `markdown-converter.json` to disable this
behavior. On **macOS**, the tool launches PDFs in **Preview** and DOCX files in
**Microsoft Word**. Generate a sample config with `generate-config.py` if
needed.

## 🔍 For Developers

The refactored architecture makes the codebase more maintainable:
- **Core logic** centralized in `markdown_utils.py`
- **Import pattern** allows legacy tools to find shared module
- **Consistent error handling** across all tools
- **Easy to extend** with new output formats

See `CLAUDE.md` for detailed development documentation.