# MarkdownConverter - Unified Conversion Tool

A single, interactive interface for converting Markdown to PDF, Word (DOCX), or LaTeX with PDF compilation.

## Features

- **Interactive Menu**: Choose your output format from a user-friendly menu
- **Multiple Formats**: Convert to PDF, Word (DOCX), or LaTeX with automatic PDF compilation
- **Organized Output**: Files are automatically organized into format-specific folders
- **Date-based Naming**: Output files use YYYYMMDD format with anti-overwrite protection
- **Dependency Checking**: Automatically detects required tools (Pandoc, pdflatex)
- **Continuous Operation**: Convert multiple files in a single session
- **Auto-Open**: Converted files open automatically after conversion. On macOS, PDFs open in Preview and DOCX files open in Microsoft Word. Set `"auto_open_output": false` to disable.

## Prerequisites

- **Python 3**
- **Pandoc**: https://pandoc.org/ (required for all conversions)
- **pdflatex**: Required for LaTeX conversion with PDF compilation (optional but recommended)

## Installation

1. Ensure prerequisites are installed
2. Make the script executable:
   ```bash
   chmod +x MarkdownConverter.py
   ```

## Usage

### Interactive Mode

Simply run the converter and follow the prompts:

```bash
./MarkdownConverter.py
```

### macOS Desktop Integration

For macOS users, desktop integration is available:

- **MarkdownConverter.app**: Double-click this app to open Terminal and automatically run the unified converter
- **MarkdownConverter.scpt**: The AppleScript source file for the launcher (can be edited in Script Editor)

### Step-by-step Process

1. **Launch the tool**:
   ```bash
   ./MarkdownConverter.py
   ```

2. **Choose output format**:
   ```
   ============================================================
   📄 Markdown Conversion Tool
   ============================================================
   Choose your output format:
     1. PDF
     2. Word (DOCX)
     3. LaTeX (with PDF compilation)
     4. Exit
   ------------------------------------------------------------
   Enter your choice (1-4): 1
   ```

3. **Paste your Markdown content**:
   ```
   Enter/paste your Markdown text.
   Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):
   ------------------------------------------------------------
   # My Document
   
   This is **bold** and this is *italic*.
   
   - List item 1
   - List item 2
   [Ctrl-D]
   ```

4. **Get your converted file**:
   ```
   🔄 Converting...
   ✅ PDF created: PDF/20250525HelloWorldThisIsMy.pdf
   
   ============================================================
   Convert another file? (y/N): 
   ```

## Output Organization

The tool automatically creates and organizes files into format-specific folders:

- **PDF files**: `PDF/20250525HelloWorldThisIsMy.pdf`, `PDF/20250525HelloWorldThisIsMy-1.pdf`, etc.
- **Word files**: `DOCX/20250525HelloWorldThisIsMy.docx`, `DOCX/20250525HelloWorldThisIsMy-1.docx`, etc.
- **LaTeX files**: `LaTeX/20250525HelloWorldThisIsMy.tex`, `LaTeX/20250525HelloWorldThisIsMy.pdf`, etc.
  - Includes compiled PDF and auxiliary files (.aux, .log)

### Auto-Open Output

Converted files open automatically after conversion. Set
`"auto_open_output": false` in your configuration file to disable this
behavior. On **macOS**, PDFs open in **Preview** and DOCX files open in
**Microsoft Word**.

## Conversion Options

### 1. PDF Conversion
- Uses Pandoc with 1-inch margins
- Output: High-quality PDF files
- Location: `PDF/` folder

### 2. Word (DOCX) Conversion  
- Uses Pandoc for maximum compatibility
- Output: Microsoft Word documents
- Location: `DOCX/` folder

### 3. LaTeX Conversion
- Generates LaTeX source files
- Automatically compiles to PDF if pdflatex is available
- Handles all auxiliary files properly
- Location: `LaTeX/` folder
- **Note**: If pdflatex is not found, only the .tex file will be generated

## Features in Detail

-### Smart File Naming
- Files include the date plus a name you provide
- Automatic increment suffix prevents overwrites
- Example: `20250525MyNotes.pdf`, `20250525MyNotes-1.pdf`

### Dependency Management
- Checks for Pandoc on startup (required)
- Detects pdflatex availability (for LaTeX conversion)
- Provides clear warnings if tools are missing

### Error Handling
- Graceful handling of conversion errors
- Option to retry after failures
- Clear error messages with suggestions

### User Experience
- Clean, intuitive menu interface
- Progress indicators during conversion
- Option to convert multiple files in one session
- Helpful emoji indicators for status

## Error Troubleshooting

### Common Issues

**"pandoc not found"**
- Install Pandoc from https://pandoc.org/
- Ensure it's in your system PATH

**"pdflatex not found"** (for LaTeX conversion)
- Install a LaTeX distribution (TeX Live, MiKTeX, etc.)
- LaTeX files will still be generated without pdflatex

**"EOF when reading a line"**
- Make sure to run the script interactively in a terminal
- Don't pipe input to the script

**Permission errors**
- Make sure the script is executable: `chmod +x MarkdownConverter.py`
- Check write permissions in the current directory

## Examples

### Converting a Simple Document
```bash
$ ./MarkdownConverter.py
Choose your output format:
  1. PDF
  2. Word (DOCX)  
  3. LaTeX (with PDF compilation)
  4. Exit
Enter your choice (1-4): 2

Enter/paste your Markdown text:
# Meeting Notes

## Attendees
- Alice
- Bob

## Action Items
1. Review proposal
2. Schedule follow-up

[Ctrl-D]

🔄 Converting...
✅ DOCX created: DOCX/20250525HelloWorldThisIsMy.docx

Convert another file? (y/N): n
👋 Goodbye!
```

### Multiple Conversions in One Session
- Choose format, paste content, convert
- Answer "y" when asked "Convert another file?"
- Repeat for different formats or content
- Exit when done

## Integration with Existing Tools

This unified converter coexists with the individual converter tools:
- `MarkdownToPDF.py` - PDF-only converter
- `MarkdownToWord.py` - Word-only converter  
- `MarkdownToLatex.py` - LaTeX-only converter

Use the unified tool for interactive conversion, or the individual tools for scripting and automation.

## Technical Details

- **Language**: Python 3
- **Dependencies**: Pandoc (required), pdflatex (optional)
- **Output**: Organized in format-specific subdirectories
- **File Handling**: Automatic directory creation, anti-overwrite protection
- **Error Handling**: Graceful failure with retry options