import os

import streamlit as st

from src.document_loader import load_document
from src.generator import generate_answer
from src.text_splitter import create_document_chunks
from src.vector_store import index_chunks, search_chunks


st.set_page_config(
    page_title="MFP Knowledge Agent",
    page_icon="💜",
    layout="wide",
)

st.title("💜 MFP Knowledge Agent")

st.write(
    "Agente inteligente para consulta do conhecimento institucional "
    "da Maratona Feminina de Programação."
)

st.caption(
    "As respostas são geradas exclusivamente com base nos documentos "
    "processados e apresentam os trechos utilizados como fonte."
)


# Configuração da API
st.sidebar.header("Configuração da IA")

cohere_api_key = st.sidebar.text_input(
    "Cohere API Key",
    type="password",
    help=(
        "Use uma Trial API Key da Cohere. "
        "A chave permanece apenas durante a sessão atual "
        "e não é armazenada pela aplicação."
    ),
)

if cohere_api_key:
    os.environ["COHERE_API_KEY"] = cohere_api_key.strip()
    st.sidebar.success("Chave configurada para esta sessão.")
else:
    st.warning(
        "Informe uma Cohere API Key na barra lateral "
        "para utilizar a aplicação."
    )
    st.stop()


# Estado da aplicação
if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0


# Upload e processamento
st.subheader("1. Envie um documento")

uploaded_file = st.file_uploader(
    "Selecione um arquivo PDF ou DOCX",
    type=["pdf", "docx"],
)

if uploaded_file is not None:
    process_document = st.button(
        "Processar documento",
        type="primary",
    )

    if process_document:
        try:
            with st.spinner(
                "Extraindo, dividindo e indexando o documento..."
            ):
                extracted_sections = load_document(uploaded_file)

                if not extracted_sections:
                    st.warning(
                        "O arquivo foi carregado, mas nenhum texto "
                        "pôde ser extraído."
                    )
                else:
                    chunks = create_document_chunks(
                        extracted_sections=extracted_sections,
                        document_name=uploaded_file.name,
                    )

                    if not chunks:
                        st.warning(
                            "Nenhum trecho válido foi criado "
                            "a partir do documento."
                        )
                    else:
                        total_indexed = index_chunks(chunks)

                        st.session_state.document_name = uploaded_file.name
                        st.session_state.document_processed = True
                        st.session_state.total_chunks = total_indexed

                        st.success(
                            "Documento processado com sucesso!"
                        )

        except Exception as error:
            st.error(
                f"Não foi possível processar o documento: {error}"
            )


# Área de perguntas
if st.session_state.document_processed:
    column_1, column_2 = st.columns(2)

    column_1.metric(
        "Documento ativo",
        st.session_state.document_name,
    )

    column_2.metric(
        "Chunks indexados",
        st.session_state.total_chunks,
    )

    st.divider()

    st.subheader("2. Faça uma pergunta")

    question = st.text_input(
        "O que você deseja saber sobre o documento?",
        placeholder=(
            "Ex.: Quais são as responsabilidades "
            "descritas no documento?"
        ),
    )

    ask_question = st.button(
        "Buscar resposta",
        disabled=not question.strip(),
    )

    if ask_question:
        try:
            with st.spinner(
                "Buscando informações e elaborando a resposta..."
            ):
                matches = search_chunks(
                    question=question,
                    number_of_results=4,
                    document_name=st.session_state.document_name,
                )

                answer = generate_answer(
                    question=question,
                    matches=matches,
                )

            st.subheader("Resposta")

            insufficient_answer = (
                "Não encontrei informações suficientes"
            )

            if answer.startswith(insufficient_answer):
                st.warning(answer)
            else:
                st.success(answer)

            st.subheader("Fontes recuperadas")

            if not matches:
                st.info(
                    "Nenhum trecho relevante foi encontrado."
                )
            else:
                for index, match in enumerate(
                    matches,
                    start=1,
                ):
                    page = (
                        match["page"]
                        if match["page"] is not None
                        else "não identificada"
                    )

                    source_title = (
                        f"Fonte {index}: "
                        f"{match['document']} | "
                        f"página {page}"
                    )

                    with st.expander(source_title):
                        st.write(match["text"])

                        st.caption(
                            f"Chunk {match['chunk_number']} | "
                            f"Distância vetorial: "
                            f"{match['distance']:.4f}"
                        )

        except Exception as error:
            st.error(
                f"Não foi possível gerar a resposta: {error}"
            )

else:
    st.info(
        "Envie e processe um documento para liberar "
        "o campo de perguntas."
    )