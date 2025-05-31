#!/usr/bin/env python3
"""
Configuration Generator for Markdown Converter Toolkit

Creates a default configuration file with user-friendly comments.
Run this script to generate markdown-converter.json in your current directory.
"""
import json
import os
from markdown_utils import get_default_config

def generate_config_file(filepath="markdown-converter.json"):
    """Generate a configuration file with default settings and comments."""
    
    config = get_default_config()
    
    # Create a commented version for user reference
    config_with_comments = {
        "_comment": "Markdown Converter Configuration - Phase 1",
        "_description": "Configure formatting options for PDF, Word, and LaTeX output",
        
        "global": {
            "_comment": "Global settings that apply to all converters",
            "save_markdown_source": config["global"]["save_markdown_source"],
            "_save_markdown_source_comment": "Save input markdown as .md file alongside converted output",
            "auto_open_output": config["global"]["auto_open_output"],
            "_auto_open_output_comment": "Automatically open converted files after conversion (set to false to disable)",
            "output_naming": config["global"]["output_naming"],
            "_output_naming_comment": "Naming scheme: 'date' (YYYYMMDD), 'prompt' (ask user), 'custom' (not implemented)"
        },
        
        "pdf": {
            "_comment": "PDF-specific formatting options",
            "geometry": {
                "margin": config["pdf"]["geometry"]["margin"],
                "_margin_comment": "Page margins (e.g., '1in', '2.5cm', '0.75in')",
                "paper": config["pdf"]["geometry"]["paper"],
                "_paper_comment": "Paper size: 'letter', 'a4', 'legal', etc."
            },
            "font": {
                "family": config["pdf"]["font"]["family"],
                "_family_comment": "Font family: 'Times New Roman', 'Arial', 'Helvetica', etc.",
                "size": config["pdf"]["font"]["size"],
                "_size_comment": "Font size: '12pt', '11pt', '14pt', etc."
            }
        },
        
        "docx": {
            "_comment": "Word document formatting options",
            "font": {
                "family": config["docx"]["font"]["family"],
                "_family_comment": "Font family for Word documents",
                "size": config["docx"]["font"]["size"],
                "_size_comment": "Font size for Word documents"
            }
        },
        
        "latex": {
            "_comment": "LaTeX document formatting options",
            "geometry": {
                "margin": config["latex"]["geometry"]["margin"],
                "_margin_comment": "Page margins for LaTeX documents",
                "paper": config["latex"]["geometry"]["paper"],
                "_paper_comment": "Paper size for LaTeX documents"
            },
            "font": {
                "family": config["latex"]["font"]["family"],
                "_family_comment": "Font family for LaTeX documents",
                "size": config["latex"]["font"]["size"],
                "_size_comment": "Font size for LaTeX documents"
            },
            "document_class": config["latex"]["document_class"],
            "_document_class_comment": "LaTeX document class: 'article', 'report', 'book', etc.",
            "compile_pdf": config["latex"]["compile_pdf"],
            "_compile_pdf_comment": "Automatically compile LaTeX to PDF (requires pdflatex)"
        }
    }
    
    # Write the configuration file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config_with_comments, f, indent=2, ensure_ascii=False)
    
    return filepath

def main():
    """Main function to generate configuration file."""
    print("🔧 Markdown Converter Configuration Generator")
    print("=" * 50)
    
    config_path = "markdown-converter.json"
    
    # Check if config already exists
    if os.path.exists(config_path):
        response = input(f"Configuration file '{config_path}' already exists. Overwrite? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ Configuration generation cancelled.")
            return
    
    try:
        generated_path = generate_config_file(config_path)
        print(f"✅ Configuration file created: {generated_path}")
        print()
        print("📝 Edit this file to customize your formatting preferences:")
        print(f"   - Margins and paper sizes for PDF/LaTeX")
        print(f"   - Font families and sizes for all formats")
        print(f"   - Enable/disable markdown source saving")
        print(f"   - Control LaTeX PDF compilation")
        print()
        print("💡 The configuration file includes helpful comments explaining each option.")
        print("💡 Remove lines starting with '_' if you want a cleaner config file.")
        
    except Exception as e:
        print(f"❌ Error creating configuration file: {e}")

if __name__ == '__main__':
    main()