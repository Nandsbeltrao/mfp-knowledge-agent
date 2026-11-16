import os

from dotenv import load_dotenv

from src.embeddings import get_cohere_client


load_dotenv()

CHAT_MODEL = os.getenv(
    "COHERE_CHAT_MODEL",
    "command-a-plus-05-2026",
)


def build_context(matches: list[dict]) -> str:
    """Organiza os trechos recuperados para envio à LLM."""

    context_parts = []

    for index, match in enumerate(matches, start=1):
        page = (
            str(match["page"])
            if match["page"] is not None
            else "não identificada"
        )

        context_parts.append(
            f"""
[FONTE {index}]
Documento: {match["document"]}
Página: {page}
Trecho: {match["text"]}
""".strip()
        )

    return "\n\n".join(context_parts)


def generate_answer(
    question: str,
    matches: list[dict],
) -> str:
    """Responde utilizando somente os trechos recuperados."""

    if not question or not question.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not matches:
        return (
            "Não encontrei informações suficientes nos documentos "
            "para responder a essa pergunta."
        )

    context = build_context(matches)
    client = get_cohere_client()

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um agente de gestão do conhecimento da "
                    "Maratona Feminina de Programação. Responda somente "
                    "com base nas fontes fornecidas. Não use conhecimento "
                    "externo e não invente informações. Se as fontes não "
                    "forem suficientes, diga exatamente: "
                    "'Não encontrei informações suficientes nos documentos "
                    "para responder a essa pergunta.' "
                    "Responda em português, de forma clara e objetiva. "
                    "Ao utilizar uma informação, indique a fonte no formato "
                    "[Fonte 1], [Fonte 2] ou equivalente."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Pergunta:\n{question}\n\n"
                    f"Fontes recuperadas:\n{context}"
                ),
            },
        ],
    )

    for content_item in response.message.content:
        text = getattr(content_item, "text", None)

        if text:
            return text

    raise ValueError(
        "A Cohere não retornou uma resposta textual."
    )