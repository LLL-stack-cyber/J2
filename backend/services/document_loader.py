"""Utilities for loading and indexing user-uploaded documents for AI tutor queries."""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict, Dict, List, Protocol, Any
from xml.etree import ElementTree
from zipfile import ZipFile
from backend.services.base import BaseAIService

logger = logging.getLogger(__name__)


class DocumentLoaderError(Exception):
    """Raised when document loading or indexing fails."""


class DocumentStore(Protocol):
    """Storage interface used by :func:`index_document` for extensibility."""

    def add(self, user_id: str, content: str) -> None: ...


class InMemoryDocumentStore:
    """Simple in-memory store for per-user text entries."""

    def __init__(self) -> None:
        self._documents: DefaultDict[str, List[str]] = defaultdict(list)

    def add(self, user_id: str, content: str) -> None:
        self._documents[user_id].append(content)

    def get(self, user_id: str) -> List[str]:
        return list(self._documents.get(user_id, []))

    def clear(self) -> None:
        self._documents.clear()


# Public in-memory index for quick retrieval. Can be replaced with DB/vector storage later.
STORE = InMemoryDocumentStore()
DOCUMENT_INDEX = STORE._documents


class DocumentLoader(BaseAIService):
    """Service for loading and cleaning document contents."""

    def __init__(self):
        super().__init__()
        self._readers: Dict[str, Callable[[Path], str]] = {
            ".txt": self._read_txt,
            ".docx": self._read_docx,
            ".pdf": self._read_pdf,
        }

    def _clean_text(self, text: str) -> str:
        """Normalize whitespace while preserving paragraph breaks."""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _read_txt(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8", errors="ignore")

    def _read_docx(self, file_path: Path) -> str:
        with ZipFile(file_path) as archive:
            document_xml = archive.read("word/document.xml")

        root = ElementTree.fromstring(document_xml)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs: List[str] = []

        for paragraph in root.findall(".//w:p", namespace):
            texts = [node.text for node in paragraph.findall(".//w:t", namespace) if node.text]
            paragraph_text = "".join(texts).strip()
            if paragraph_text:
                paragraphs.append(paragraph_text)

        return "\n\n".join(paragraphs)

    def _read_pdf(self, file_path: Path) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:  # pragma: no cover - depends on optional dependency
            raise DocumentLoaderError(
                "PDF support requires the 'pypdf' package. Install with: pip install pypdf"
            ) from exc

        reader = PdfReader(str(file_path))
        page_text = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(page_text)

    def load_document(self, file_path: str) -> Dict[str, Any]:
        """Load a PDF, DOCX, or TXT file and return cleaned text content."""
        try:
            path = Path(file_path)

            if not path.exists() or not path.is_file():
                return self._error_response(f"File not found: {file_path}")

            extension = path.suffix.lower()
            reader = self._readers.get(extension)
            if not reader:
                return self._error_response(f"Unsupported file format: {extension}")

            raw_text = reader(path)
            cleaned_text = self._clean_text(raw_text)
            return self._standardize_response(cleaned_text)
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return self._error_response(f"Failed to load document: {str(e)}")

# Keep functional interface for backward compatibility if needed, but point to DocumentLoader
_loader = DocumentLoader()

def load_document(file_path: str) -> str:
    """Backward compatible function that returns string content."""
    res = _loader.load_document(file_path)
    if res.get("status") == "success":
        return res.get("data", "")
    return ""
