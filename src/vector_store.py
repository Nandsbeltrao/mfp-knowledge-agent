from pathlib import Path

import chromadb

from src.embeddings import generate_embeddings


DATABASE_PATH = Path("chroma_db")
COLLECTION_NAME = "mfp_knowledge"


def get_collection():
    """Cria ou recupera a coleção do banco vetorial."""

    client = chromadb.PersistentClient(
        path=str(DATABASE_PATH)
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_chunks(chunks: list[dict]) -> int:
    """Gera embeddings e armazena os chunks no ChromaDB."""

    if not chunks:
        raise ValueError(
            "Nenhum chunk foi fornecido para indexação."
        )

    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(
        texts=texts,
        input_type="search_document",
    )

    ids = [chunk["id"] for chunk in chunks]

    metadatas = [
        {
            "document": chunk["document"],
            "page": (
                chunk["page"]
                if chunk["page"] is not None
                else -1
            ),
            "chunk_number": chunk["chunk_number"],
        }
        for chunk in chunks
    ]

    collection = get_collection()

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)


def search_chunks(
    question: str,
    number_of_results: int = 4,
    document_name: str | None = None,
) -> list[dict]:
    """Busca os chunks semanticamente mais próximos da pergunta."""

    if not question or not question.strip():
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = generate_embeddings(
        texts=[question],
        input_type="search_query",
    )[0]

    query_parameters = {
        "query_embeddings": [query_embedding],
        "n_results": min(
            number_of_results,
            collection.count(),
        ),
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    if document_name:
        query_parameters["where"] = {
            "document": document_name,
        }

    result = collection.query(**query_parameters)

    matches = []

    if not result["documents"] or not result["documents"][0]:
        return matches

    for document, metadata, distance in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    ):
        matches.append(
            {
                "text": document,
                "document": metadata["document"],
                "page": (
                    None
                    if metadata["page"] == -1
                    else metadata["page"]
                ),
                "chunk_number": metadata["chunk_number"],
                "distance": distance,
            }
        )

    return matches