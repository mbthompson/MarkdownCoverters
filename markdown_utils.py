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
import re


def get_unique_filename(basename):
    """
    Generate a filename that does not overwrite existing files.
    E.g., for basename 'PDF/20250525HelloWorld.pdf', returns
    'PDF/20250525HelloWorld.pdf' or 'PDF/20250525HelloWorld-1.pdf', etc.
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


def get_markdown_input(prompt=None):
    """Get Markdown text from user input via stdin."""
    if prompt is None:
        prompt = (
            "Enter/paste your Markdown text.\n"
            "Finish with Ctrl-D (Unix/macOS) or Ctrl-Z then Enter (Windows):\n"
        )

    if prompt:
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


def get_snippet_slug(text, num_words=6):
    """Return a CamelCase slug of the first `num_words` words in `text`."""
    words = re.findall(r'[A-Za-z0-9]+', text)
    snippet_words = words[:num_words]
    return ''.join(word.capitalize() for word in snippet_words)


def get_dated_filename(output_dir, extension, markdown_text=None, custom_slug=None):
    """Generate a date-based filename with an optional custom slug."""
    today_str = datetime.date.today().strftime('%Y%m%d')

    if custom_slug:
        slug = get_snippet_slug(custom_slug)
    else:
        slug = get_snippet_slug(markdown_text) if markdown_text else ''

    base_name = f"{today_str}{slug}"

    default_file = os.path.join(output_dir, f"{base_name}.{extension}")
    return get_unique_filename(default_file)


def save_markdown_file(markdown_text, output_file_path):
    """
    Save the input markdown text as a .md file with the same base name as the output file.
    
    Args:
        markdown_text: String containing the markdown content
        output_file_path: Path to the converted output file (e.g., 'PDF/20250525HelloWorld.pdf')
        
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


def open_file(path):
    """Open a file using the default application for the current OS."""
    try:
        abs_path = os.path.abspath(path)
        if sys.platform.startswith('darwin'):
            ext = os.path.splitext(abs_path)[1].lower()
            if ext == '.pdf':
                subprocess.run(['open', '-a', 'Preview', abs_path], check=False)
            elif ext == '.docx':
                subprocess.run(['open', '-a', 'Microsoft Word', abs_path], check=False)
            else:
                subprocess.run(['open', abs_path], check=False)
        elif os.name == 'nt':
            os.startfile(abs_path)  # type: ignore[attr-defined]
        else:
            subprocess.run(['xdg-open', abs_path], check=False)
    except Exception:
        pass


def get_default_config():
    """Return default configuration settings."""
    return {
        "global": {
            "save_markdown_source": True,
            "auto_open_output": True,
            "output_naming": "date"
        },
        "pdf": {
            "geometry": {
                "margin": "1in",
                "paper": "letter"
            },
            "font": {
                "family": "Latin Modern Roman",
                "size": "10pt"
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
                "family": "Latin Modern Roman",
                "size": "10pt"
            },
            "document_class": "article",
            "compile_pdf": True
        }
    }


def deep_merge(base, override):
    """Recursively merge two dictionaries (override into base)."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def load_config():
    """
    Load configuration from file with fallback to defaults.
    
    Searches for config files in this order:
    1. ./markdown-converter.json (current directory)
    2. ~/markdown-converter.json (home directory)
    3. Default configuration (built-in)
    
    Returns:
        dict: Configuration settings
    """
    default_config = get_default_config()
    
    # Look for configuration in the current directory first, then the home directory
    config_paths = [
        "./markdown-converter.json",
        os.path.expanduser("~/markdown-converter.json")
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge user config with defaults using deep merge
                    merged_config = deep_merge(default_config.copy(), user_config)
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
