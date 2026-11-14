from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(file) -> list[dict]:
    """Extrai o texto de um PDF, preservando o número de cada página."""

    reader = PdfReader(file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append(
                {
                    "text": text.strip(),
                    "page": page_number,
                }
            )

    return pages


def extract_text_from_docx(file) -> list[dict]:
    """Extrai os parágrafos com conteúdo de um documento DOCX."""

    document = Document(file)

    text = "\n".join(
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    if not text:
        return []

    return [
        {
            "text": text,
            "page": None,
        }
    ]


def load_document(file) -> list[dict]:
    """Identifica a extensão do arquivo e executa a extração adequada."""

    extension = Path(file.name).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file)

    if extension == ".docx":
        return extract_text_from_docx(file)

    raise ValueError(
        "Formato não suportado. Envie um arquivo PDF ou DOCX."
    )