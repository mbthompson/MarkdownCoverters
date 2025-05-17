# Project Title

A brief description of the project.

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

How to use this project.

### Generate a sample DOCX

This project includes a script to generate a Word document (`sample.docx`) with headings and sample text.

```bash
python generate_docx.py
```

## LaTeX Starter Template

This project includes a basic LaTeX template and a script to generate a `.tex` file using PyLaTeX.

### Using the provided template
1. Edit `template.tex` as needed.
2. Compile to PDF:
   ```bash
   latexmk -pdf template.tex
   ```

### Generating a .tex file via Python
1. Ensure PyLaTeX is installed:
   ```bash
   pip install pylatex
   ```
2. Run the generation script:
   ```bash
   python generate_tex.py
   ```
3. Compile the generated file:
   ```bash
   latexmk -pdf generated.tex
   ```