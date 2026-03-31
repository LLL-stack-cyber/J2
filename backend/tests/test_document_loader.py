from pathlib import Path
from zipfile import ZipFile

import pytest

from backend.services.document_loader import (
    DOCUMENT_INDEX,
    DocumentLoaderError,
    index_document,
    load_document,
)


def test_load_txt_document(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Line 1\n\n\nLine 2", encoding="utf-8")

    content = load_document(str(file_path))

    assert content == "Line 1\n\nLine 2"


def test_load_docx_document(tmp_path: Path):
    docx_path = tmp_path / "notes.docx"
    xml = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"
        "<w:body>"
        "<w:p><w:r><w:t>First paragraph.</w:t></w:r></w:p>"
        "<w:p><w:r><w:t>Second paragraph.</w:t></w:r></w:p>"
        "</w:body></w:document>"
    )

    with ZipFile(docx_path, "w") as archive:
        archive.writestr("word/document.xml", xml)

    content = load_document(str(docx_path))

    assert content == "First paragraph.\n\nSecond paragraph."


def test_unsupported_document_extension(tmp_path: Path):
    file_path = tmp_path / "notes.md"
    file_path.write_text("hello", encoding="utf-8")

    with pytest.raises(DocumentLoaderError, match="Unsupported file type"):
        load_document(str(file_path))


def test_missing_file_raises_error(tmp_path: Path):
    with pytest.raises(DocumentLoaderError, match="File not found"):
        load_document(str(tmp_path / "missing.txt"))


def test_index_document_stores_text_by_user():
    DOCUMENT_INDEX.clear()

    index_document("user-1", "  Example   text\n\n\nfor indexing ")

    assert DOCUMENT_INDEX["user-1"] == ["Example text\n\nfor indexing"]


def test_index_document_rejects_empty_payload():
    with pytest.raises(DocumentLoaderError, match="text_content cannot be empty"):
        index_document("user-1", "   \n\n")
