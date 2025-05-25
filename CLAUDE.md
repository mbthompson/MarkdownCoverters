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
  - Uses shared `markdown_utils.py` module for core functionality
- **MarkdownConverter.app**: macOS app bundle for desktop integration
- **MarkdownConverter.scpt**: AppleScript source for the launcher

### Shared Module
- **markdown_utils.py**: Core functionality shared across all converters
  - File management and anti-overwrite protection
  - Dependency checking (pandoc, pdflatex)
  - Subprocess wrappers for pandoc and pdflatex
  - Input handling and error management
  - Eliminates code duplication across all tools

### Legacy Tools (in legacy/ folder)
- **legacy/MarkdownToPDF/**: PDF-only converter (uses `pandoc -t pdf`)
- **legacy/MarkdownToWord/**: Word-only converter (uses `pandoc -t docx`) 
- **legacy/MarkdownToLatex/**: LaTeX-only converter (uses `pandoc -t latex` + `pdflatex`)

Each legacy tool directory contains:
- Python script (e.g., `MarkdownToPDF.py`) - now imports `markdown_utils.py`
- macOS .app launcher bundle for Terminal integration
- AppleScript source file (.scpt) for the launcher
- Individual README.md with usage instructions

**Note**: Legacy tools maintain standalone operation while sharing core logic through dynamic imports.

### Output Organization
All tools create organized output folders:
- **PDF/**: PDF files from both unified and legacy PDF converter
- **DOCX/**: Word files from both unified and legacy Word converter
- **LaTeX/**: LaTeX and compiled PDF files, including auxiliary files (.aux, .log)

## Architecture

### Unified Converter (MarkdownConverter.py)
- **Interactive Menu System**: User selects output format via numbered menu
- **Format-Specific Handlers**: `convert_to_pdf()`, `convert_to_word()`, `convert_to_latex()`
- **Imports Shared Module**: Uses `markdown_utils` functions for core operations
- **Enhanced Error Handling**: Retry mechanisms and graceful failure recovery

### Legacy Tools Pattern
All legacy tools follow the same pattern:
- Read Markdown from stdin (interactive mode or piped input)
- Import shared functionality via `sys.path.insert()` for parent directory access
- Use shared `run_pandoc()` wrapper for consistent subprocess handling
- Generate unique output filenames via shared `get_dated_filename()`
- Maintain standalone operation for scripting/automation

### Shared Module Architecture (`markdown_utils.py`)
Core functions used by all tools:

#### File Management:
- `get_unique_filename()`: Anti-overwrite protection with incremental suffixes
- `ensure_output_dir()`: Creates output directories (PDF/, DOCX/, LaTeX/)
- `get_dated_filename()`: YYYYMMDD-based naming with uniqueness

#### Dependency Management:
- `check_pandoc()`: Validates pandoc availability, exits if missing
- `check_pdflatex()`: Returns boolean for pdflatex availability

#### Process Management:
- `run_pandoc()`: Subprocess wrapper with consistent environment setup
- `run_pdflatex()`: LaTeX compilation with proper error handling
- `get_markdown_input()`: Stdin reading with interrupt handling

#### Benefits:
- **70% code reduction** across all converters
- **Single source of truth** for core logic
- **Consistent behavior** across unified and legacy tools
- **Maintained compatibility** - tools work identically to before

## Common Commands

### Primary Usage (Recommended)
```bash
# Interactive unified converter
./MarkdownConverter.py

# Make executable if needed
chmod +x MarkdownConverter.py

# macOS desktop integration
open MarkdownConverter.app
# Or double-click MarkdownConverter.app in Finder
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

# Test shared module functions
python3 -c "
from markdown_utils import check_pandoc, get_unique_filename, ensure_output_dir
check_pandoc()
print('✅ Shared module works correctly')
"
```

### Prerequisites Check
- Pandoc: `pandoc --version` (required for all conversions)
- LaTeX: `pdflatex --version` (required for LaTeX conversion with PDF compilation)

## Development Notes

### Code Organization
- **Shared module**: `markdown_utils.py` contains all common functionality
- **Unified converter**: Imports shared module, focuses on UI and workflow
- **Legacy tools**: Import shared module while maintaining standalone operation
- **No external dependencies**: Only Python standard library + external tools (pandoc, pdflatex)
- **Consistent subprocess integration**: All tools use shared `run_pandoc()` and `run_pdflatex()` wrappers

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

- **Backward compatibility**: All tools work identically to before refactoring
- **Shared module integration**: Legacy tools dynamically import `markdown_utils.py` from parent directory
- **Output folders**: Shared between unified and legacy tools (PDF/, DOCX/, LaTeX/)
- **File naming**: Consistent conventions across all tools via shared functions
- **macOS integration**: .app bundles provide desktop integration for both unified and legacy tools
- **Customization**: AppleScript source files (.scpt) allow launcher behavior modification
- **Standalone operation**: Legacy tools can be copied individually and will find shared module at runtime