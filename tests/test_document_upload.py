from io import BytesIO
from pathlib import Path

from src.document_loader import load_document


class UploadedFileSimulation(BytesIO):
    """Simula o objeto entregue pelo st.file_uploader."""

    def __init__(self, file_path: Path):
        file_bytes = file_path.read_bytes()

        super().__init__(file_bytes)

        self.name = file_path.name


def test_docx_upload():
    file_path = Path("data/sample/teste.docx")

    uploaded_file = UploadedFileSimulation(file_path)

    sections = load_document(uploaded_file)

    assert sections
    assert sections[0]["text"].strip()

    print(
        f"DOCX validado: {len(sections)} seção, "
        f"{len(sections[0]['text'])} caracteres."
    )


def test_pdf_upload():
    file_path = Path("data/sample/teste2.pdf")

    uploaded_file = UploadedFileSimulation(file_path)

    sections = load_document(uploaded_file)

    assert sections
    assert sections[0]["text"].strip()
    assert sections[0]["page"] == 1

    print(
        f"PDF validado: {len(sections)} página, "
        f"{len(sections[0]['text'])} caracteres."
    )


if __name__ == "__main__":
    test_docx_upload()
    test_pdf_upload()

    print("Upload simulado validado com sucesso.")