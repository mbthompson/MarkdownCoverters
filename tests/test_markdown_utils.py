import os
import subprocess
import subprocess
from unittest.mock import patch

from markdown_utils import run_pandoc, run_pdflatex


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
