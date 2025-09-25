import os
import subprocess
import subprocess
from unittest.mock import patch

from markdown_utils import run_pandoc, run_pdflatex, sanitize_text


def test_run_pandoc_returns_false_on_error(tmp_path):
    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, stdout=b'', stderr=b'error')

    with patch('subprocess.run', side_effect=fake_run):
        assert not run_pandoc(['pandoc', '-o', 'out.pdf'], 'content')


def test_run_pdflatex_error_pdf_generated(tmp_path):
    tex_file = tmp_path / 'doc.tex'
    tex_file.write_text('test')
    pdf_file = tmp_path / 'doc.pdf'
    pdf_file.write_text('pdf')

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, stdout=b'', stderr=b'latex error')

    with patch('subprocess.run', side_effect=fake_run):
        success, result_pdf = run_pdflatex(str(tex_file), str(tmp_path))

    assert success
    assert result_pdf == str(pdf_file)


def test_run_pdflatex_error_no_pdf(tmp_path):
    tex_file = tmp_path / 'doc.tex'
    tex_file.write_text('test')

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, stdout=b'', stderr=b'latex error')

    with patch('subprocess.run', side_effect=fake_run):
        success, result_pdf = run_pdflatex(str(tex_file), str(tmp_path))

    assert not success
    assert result_pdf is None

def test_sanitize_text_removes_non_ascii_and_emoji():
    # Remove emoji and special characters, preserving ASCII content
    assert sanitize_text("Hello 🐍!") == "Hello !"
    # Em dash turns into two hyphens
    assert sanitize_text("Café — Rocket 🚀!") == "Caf -- Rocket !"
    # Common math and punctuation replacements
    assert sanitize_text("a ≠ b") == "a != b"
    assert sanitize_text("x ≤ y ≥ z") == "x <= y >= z"
    # Approximately equal symbol
    assert sanitize_text("a ≈ b") == "a ~= b"
    assert sanitize_text("Quote: “text” and ‘more’") == "Quote: \"text\" and 'more'"
