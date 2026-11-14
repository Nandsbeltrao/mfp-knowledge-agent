def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """Divide um texto em chunks com sobreposição."""

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size deve ser maior que zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap não pode ser negativo.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap deve ser menor que chunk_size."
        )

    normalized_text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(normalized_text):
        end = start + chunk_size
        chunk = normalized_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(normalized_text):
            break

        start = end - chunk_overlap

    return chunks


def create_document_chunks(
    extracted_sections: list[dict],
    document_name: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """Cria chunks preservando os metadados do documento."""

    document_chunks = []
    chunk_number = 1

    for section in extracted_sections:
        section_chunks = split_text(
            text=section["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for text in section_chunks:
            document_chunks.append(
                {
                    "id": f"{document_name}-{chunk_number}",
                    "document": document_name,
                    "page": section.get("page"),
                    "chunk_number": chunk_number,
                    "text": text,
                }
            )

            chunk_number += 1

    return document_chunks