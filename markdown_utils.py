#!/usr/bin/env python3
"""
Markdown Utilities - Shared logic for Markdown conversion tools

Common functionality used by both the unified MarkdownConverter 
and legacy individual conversion tools.
"""
import sys
import os
import shutil
import subprocess
import datetime
import json


def get_unique_filename(basename):
    """
    Generate a filename that does not overwrite existing files.
    E.g., for basename 'PDF/20250525.pdf', returns 'PDF/20250525.pdf' or 'PDF/20250525-1.pdf', etc.
    """
    base, ext = os.path.splitext(basename)
    filename = basename
    index = 1
    while os.path.exists(filename):
        filename = f"{base}-{index}{ext}"
        index += 1
    return filename


def check_pandoc():
    """Check if pandoc is available."""
    if shutil.which('pandoc') is None:
        sys.exit("Error: pandoc not found. Please install pandoc and retry.")


def check_pdflatex():
    """Check if pdflatex is available."""
    return shutil.which('pdflatex') is not None


def get_markdown_input():
    """Get Markdown text from user input via stdin."""
    prompt = (
        "Enter/paste your Markdown text.\n"
        "Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):\n"
    )
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    try:
        markdown_text = sys.stdin.read()
    except KeyboardInterrupt:
        sys.exit("\nInput cancelled. Exiting.")
    
    if not markdown_text.strip():
        sys.exit("No input received. Exiting.")
    
    return markdown_text


def ensure_output_dir(output_dir):
    """Ensure output directory exists."""
    os.makedirs(output_dir, exist_ok=True)


def get_dated_filename(output_dir, extension):
    """Generate a date-based filename in the specified directory."""
    today_str = datetime.date.today().strftime('%Y%m%d')
    default_file = os.path.join(output_dir, f'{today_str}.{extension}')
    return get_unique_filename(default_file)


def save_markdown_file(markdown_text, output_file_path):
    """
    Save the input markdown text as a .md file with the same base name as the output file.
    
    Args:
        markdown_text: String containing the markdown content
        output_file_path: Path to the converted output file (e.g., 'PDF/20250525.pdf')
        
    Returns:
        str: Path to the saved markdown file
    """
    # Get the base name without extension and change extension to .md
    base_path = os.path.splitext(output_file_path)[0]
    md_filename = f"{base_path}.md"
    
    try:
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        return md_filename
    except Exception as e:
        print(f"Warning: Failed to save markdown file {md_filename}: {e}")
        return None


def run_pandoc(command_args, markdown_text):
    """
    Run pandoc with the given command arguments and markdown input.
    
    Args:
        command_args: List of pandoc command arguments
        markdown_text: String containing markdown content
        
    Returns:
        None (raises SystemExit on failure)
    """
    try:
        # Set TMPDIR to current directory for pandoc temp files
        env = os.environ.copy()
        env['TMPDIR'] = os.getcwd()
        
        subprocess.run(
            command_args,
            input=markdown_text.encode('utf-8'),
            check=True,
            env=env
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc failed with exit code {e.returncode}.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")


def run_pdflatex(tex_file, output_dir):
    """
    Run pdflatex to compile a .tex file to PDF.
    
    Args:
        tex_file: Path to the .tex file
        output_dir: Directory for output files
        
    Returns:
        tuple: (success: bool, pdf_file: str or None)
    """
    pdf_file = os.path.splitext(tex_file)[0] + ".pdf"
    
    try:
        env = os.environ.copy()
        env['TMPDIR'] = os.getcwd()
        
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', tex_file],
            check=True,
            env=env
        )
        return True, pdf_file
    except subprocess.CalledProcessError as e:
        return False, None


def get_default_config():
    """Return default configuration settings."""
    return {
        "global": {
            "save_markdown_source": True,
            "auto_open_output": False,
            "output_naming": "date"
        },
        "pdf": {
            "geometry": {
                "margin": "1in",
                "paper": "letter"
            },
            "font": {
                "family": "Times New Roman",
                "size": "12pt"
            }
        },
        "docx": {
            "font": {
                "family": "Times New Roman", 
                "size": "12pt"
            }
        },
        "latex": {
            "geometry": {
                "margin": "1in",
                "paper": "letter"
            },
            "font": {
                "family": "Times New Roman",
                "size": "12pt"
            },
            "document_class": "article",
            "compile_pdf": True
        }
    }


def load_config():
    """
    Load configuration from file with fallback to defaults.
    
    Searches for config files in this order:
    1. ./markdown-converter.json (current directory, visible)
    2. ./.markdown-converter.json (current directory, hidden - legacy)
    3. ~/markdown-converter.json (home directory, visible)
    4. ~/.markdown-converter.json (home directory, hidden - legacy)
    5. Default configuration (built-in)
    
    Returns:
        dict: Configuration settings
    """
    default_config = get_default_config()
    
    # Try visible files first, then hidden files for backward compatibility
    config_paths = [
        "./markdown-converter.json",                      # Visible (new, preferred)
        "./.markdown-converter.json",                     # Hidden (legacy)
        os.path.expanduser("~/markdown-converter.json"),  # Visible home (new)
        os.path.expanduser("~/.markdown-converter.json")  # Hidden home (legacy)
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge user config with defaults (user config takes precedence)
                    merged_config = default_config.copy()
                    for section, settings in user_config.items():
                        if section in merged_config:
                            if isinstance(settings, dict):
                                merged_config[section].update(settings)
                            else:
                                merged_config[section] = settings
                        else:
                            merged_config[section] = settings
                    return merged_config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")
                continue
    
    # Return defaults if no valid config file found
    return default_config


def build_pandoc_args(base_args, format_config):
    """
    Build pandoc arguments from base args and configuration.
    
    Args:
        base_args: List of base pandoc arguments
        format_config: Configuration dict for the specific format
        
    Returns:
        List: Complete pandoc arguments with config applied
    """
    args = base_args.copy()
    
    # Add geometry settings for PDF and LaTeX
    if 'geometry' in format_config:
        geometry = format_config['geometry']
        margin = geometry.get('margin', '1in')
        paper = geometry.get('paper', 'letter')
        geometry_str = f"margin={margin},paper={paper}"
        
        # Replace existing geometry argument or add new one
        geometry_found = False
        for i, arg in enumerate(args):
            if arg == '-V' and i + 1 < len(args) and args[i + 1].startswith('geometry:'):
                args[i + 1] = f'geometry:{geometry_str}'
                geometry_found = True
                break
        
        if not geometry_found:
            args.extend(['-V', f'geometry:{geometry_str}'])
    
    # Add font settings
    if 'font' in format_config:
        font = format_config['font']
        family = font.get('family')
        size = font.get('size')
        
        if family:
            args.extend(['-V', f'mainfont:{family}'])
        if size:
            args.extend(['-V', f'fontsize:{size}'])
    
    return args