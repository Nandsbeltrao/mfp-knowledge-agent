import os

from dotenv import load_dotenv

from src.embeddings import get_cohere_client


load_dotenv()

CHAT_MODEL = os.getenv(
    "COHERE_CHAT_MODEL",
    "command-a-plus-05-2026",
)

INSUFFICIENT_INFORMATION_MESSAGE = (
    "Não encontrei informações suficientes nos documentos "
    "para responder a essa pergunta."
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


def extract_text_from_response(response) -> str:
    """Extrai o conteúdo textual retornado pela Cohere."""

    for content_item in response.message.content:
        text = getattr(content_item, "text", None)

        if text:
            return text.strip()

    raise ValueError(
        "A Cohere não retornou uma resposta textual."
    )


def generate_answer(
    question: str,
    matches: list[dict],
) -> str:
    """Responde utilizando somente os trechos recuperados."""

    if not question or not question.strip():
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    if not matches:
        return INSUFFICIENT_INFORMATION_MESSAGE

    context = build_context(matches)
    client = get_cohere_client()

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um agente de gestão do conhecimento da "
                    "Maratona Feminina de Programação. Responda "
                    "exclusivamente com base nas fontes fornecidas. "
                    "Não utilize conhecimento externo e nunca invente "
                    "nomes, ferramentas, responsáveis, prazos ou valores. "

                    "Antes de responder, classifique internamente a situação "
                    "como uma das seguintes opções: "
                    "1. resposta completa; "
                    "2. resposta parcial; "
                    "3. ausência total de informação. "

                    "Se houver qualquer informação relacionada à pergunta "
                    "nas fontes, mesmo que incompleta, apresente essa "
                    "informação e explique claramente qual detalhe não foi "
                    "especificado. "

                    "Por exemplo, se o documento mencionar uma lista de "
                    "tarefas, mas não informar qual ferramenta organiza "
                    "essa lista, diga que uma lista de tarefas é exigida, "
                    "porém a ferramenta não foi especificada. "
                    "Não trate esse caso como ausência total de informação. "

                    "Use a frase de insuficiência somente quando as fontes "
                    "não contiverem nenhuma informação relacionada à "
                    "pergunta. Nesse caso, responda exatamente: "
                    f"'{INSUFFICIENT_INFORMATION_MESSAGE}' "

                    "Responda em português, de forma clara e objetiva. "
                    "Toda afirmação baseada nas fontes deve indicar a "
                    "referência no formato [Fonte 1], [Fonte 2] "
                    "ou equivalente."
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

    return extract_text_from_response(response)