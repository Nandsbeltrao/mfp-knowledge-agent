import os

import cohere
from dotenv import load_dotenv


load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "COHERE_EMBEDDING_MODEL",
    "embed-v5.0-fast",
)


def get_cohere_client() -> cohere.ClientV2:
    """Cria o cliente da Cohere usando a chave do arquivo .env."""

    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError(
            "A variável COHERE_API_KEY não foi encontrada."
        )

    return cohere.ClientV2(api_key=api_key)


def generate_embeddings(
    texts: list[str],
    input_type: str = "search_document",
) -> list[list[float]]:
    """Gera embeddings para documentos ou perguntas."""

    valid_texts = [
        text.strip()
        for text in texts
        if text and text.strip()
    ]

    if not valid_texts:
        raise ValueError(
            "É necessário fornecer pelo menos um texto válido."
        )

    client = get_cohere_client()

    inputs = [
        {
            "content": [
                {
                    "type": "text",
                    "text": text,
                }
            ]
        }
        for text in valid_texts
    ]

    response = client.embed(
        model=EMBEDDING_MODEL,
        inputs=inputs,
        input_type=input_type,
        embedding_types=["float"],
    )

    return response.embeddings.float_