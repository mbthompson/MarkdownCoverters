# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a Markdown Conversion Toolkit with a **unified interactive converter** as the primary interface and legacy individual tools for specialized use cases.

### Primary Tool
- **MarkdownConverter.py**: Unified interactive converter with menu system
  - Supports PDF, Word (DOCX), and LaTeX output formats
  - Interactive format selection (1=PDF, 2=Word, 3=LaTeX)
  - Continuous operation mode for multiple conversions
  - Comprehensive error handling and dependency checking

### Legacy Tools (in legacy/ folder)
- **legacy/MarkdownToPDF/**: PDF-only converter (uses `pandoc -t pdf`)
- **legacy/MarkdownToWord/**: Word-only converter (uses `pandoc -t docx`) 
- **legacy/MarkdownToLatex/**: LaTeX-only converter (uses `pandoc -t latex` + `pdflatex`)

Each legacy tool directory contains:
- Python script (e.g., `MarkdownToPDF.py`)
- macOS .app launcher bundle for Terminal integration
- AppleScript source file (.scpt) for the launcher
- Individual README.md with usage instructions

### Output Organization
All tools create organized output folders:
- **PDF/**: PDF files from both unified and legacy PDF converter
- **DOCX/**: Word files from both unified and legacy Word converter
- **LaTeX/**: LaTeX and compiled PDF files, including auxiliary files (.aux, .log)

## Architecture

### Unified Converter (MarkdownConverter.py)
- **Interactive Menu System**: User selects output format via numbered menu
- **Shared Core Functions**: Consolidates common functionality from legacy tools
- **Format-Specific Handlers**: `convert_to_pdf()`, `convert_to_word()`, `convert_to_latex()`
- **Smart File Management**: Auto-creates output directories, handles overwrites
- **Dependency Detection**: Checks for pandoc (required) and pdflatex (optional)

### Legacy Tools Pattern
All legacy tools follow the same pattern:
- Read Markdown from stdin (interactive mode or piped input)
- Use Pandoc subprocess calls for conversion
- Generate unique output filenames to avoid overwrites
- Set TMPDIR to current directory for Pandoc temp files
- Handle errors gracefully with informative messages

### Shared Functionality
Key functions across all tools:
- `get_unique_filename()`: Prevents file overwrites by appending incrementing numbers
- Date-based naming: YYYYMMDD format with incremental suffixes
- Pandoc integration: All tools require Pandoc on PATH
- LaTeX compilation: LaTeX tools require pdflatex for PDF generation

## Common Commands

### Primary Usage (Recommended)
```bash
# Interactive unified converter
./MarkdownConverter.py

# Make executable if needed
chmod +x MarkdownConverter.py
```

### Legacy Tools (for scripting/automation)
```bash
# Make scripts executable
chmod +x legacy/MarkdownToPDF/MarkdownToPDF.py
chmod +x legacy/MarkdownToWord/MarkdownToWord.py  
chmod +x legacy/MarkdownToLatex/MarkdownToLatex.py

# Interactive mode
./legacy/MarkdownToPDF/MarkdownToPDF.py

# File mode (good for scripts)
cat mydoc.md | ./legacy/MarkdownToWord/MarkdownToWord.py
```

### Testing All Formats
```bash
# Test unified converter programmatically
python3 -c "
from MarkdownConverter import convert_to_pdf, convert_to_word, convert_to_latex, check_dependencies
# Test conversions here
"
```

### Prerequisites Check
- Pandoc: `pandoc --version` (required for all conversions)
- LaTeX: `pdflatex --version` (required for LaTeX conversion with PDF compilation)

## Development Notes

### Code Organization
- **Unified converter**: Single file with consolidated functionality
- **Legacy tools**: Independent scripts with no shared modules
- **No external dependencies**: Only Python standard library + external tools (pandoc, pdflatex)
- **Subprocess integration**: All conversions use subprocess to call pandoc/pdflatex

### File Management
- **Date-based naming**: YYYYMMDD format across all tools
- **Anti-overwrite protection**: Automatic increment suffixes (-1, -2, etc.)
- **Organized output**: Format-specific folders (PDF/, DOCX/, LaTeX/)
- **Auxiliary file handling**: LaTeX tools properly manage .aux, .log files in LaTeX/ folder

### Error Handling
- **Dependency checking**: Graceful handling of missing pandoc/pdflatex
- **Conversion failures**: Clear error messages with suggestions
- **User interruption**: Proper handling of Ctrl-C during input
- **Retry mechanisms**: Unified converter allows retry after failures

### User Experience
- **Interactive menus**: Clear format selection with numbered options
- **Progress indicators**: Status messages with emoji indicators
- **Continuous operation**: Option to convert multiple files in one session
- **Help text**: Clear instructions for input methods (Ctrl-D, etc.)

## When to Use Which Tool

### Use Unified Converter (MarkdownConverter.py) for:
- Interactive document conversion
- Users who work with multiple output formats
- When you want guided, user-friendly experience
- One-off conversions with immediate feedback

### Use Legacy Tools for:
- Scripting and automation
- CI/CD pipelines
- When you only need one specific format
- Programmatic integration where you know the target format
- Batch processing scripts

## Integration Notes

- All tools maintain backward compatibility
- Output folders are shared between unified and legacy tools
- File naming conventions are consistent across all tools
- macOS .app bundles in legacy tools provide desktop integration