import os
from pathlib import Path

import streamlit as st

from src.document_loader import load_document
from src.generator import generate_answer
from src.text_splitter import create_document_chunks
from src.vector_store import index_chunks, search_chunks


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================


def load_css(css_path: str) -> None:
    """Carrega um arquivo CSS externo na aplicação."""

    css_file = Path(css_path)

    if not css_file.exists():
        st.warning(
            f"O arquivo de estilo não foi encontrado: {css_path}"
        )
        return

    css_content = css_file.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


def show_api_key_warning() -> None:
    """Exibe o aviso personalizado para configuração da API."""

    st.markdown(
        """
        <div class="mfp-api-warning">
            Informe uma Cohere API Key na barra lateral
            para utilizar a aplicação.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================


st.set_page_config(
    page_title="MFP Knowledge Agent",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css("assets/styles.css")


# =========================================================
# CABEÇALHO
# =========================================================


st.title("🦜 MFP Knowledge Agent")

st.write(
    "Agente inteligente para consulta do conhecimento institucional "
    "da Maratona Feminina de Programação."
)

st.caption(
    "As respostas são geradas exclusivamente com base nos documentos "
    "processados e apresentam os trechos utilizados como fonte."
)


# =========================================================
# CONFIGURAÇÃO DA IA
# =========================================================


st.sidebar.header("Configuração da IA")

st.sidebar.caption(
    "Informe uma Trial API Key da Cohere para utilizar o agente."
)

cohere_api_key = st.sidebar.text_input(
    "Cohere API Key",
    type="password",
    help=(
        "A chave permanece somente durante a sessão atual "
        "e não é armazenada pela aplicação."
    ),
)

if cohere_api_key:
    os.environ["COHERE_API_KEY"] = cohere_api_key.strip()

    st.sidebar.success(
        "Chave configurada para esta sessão."
    )

else:
    show_api_key_warning()
    st.stop()


# =========================================================
# ESTADO DA APLICAÇÃO
# =========================================================


if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0


# =========================================================
# ESCOLHA DO DOCUMENTO
# =========================================================


st.subheader("1. Escolha um documento")

input_mode = st.radio(
    "Como deseja fornecer o documento?",
    options=[
        "Usar arquivo de teste do projeto",
        "Enviar PDF ou DOCX",
    ],
)

document_to_process = None
document_name = None


if input_mode == "Usar arquivo de teste do projeto":
    sample_directory = Path("data/sample")

    sample_files = []

    if sample_directory.exists():
        sample_files = sorted(
            list(sample_directory.glob("*.pdf"))
            + list(sample_directory.glob("*.docx"))
        )

    if not sample_files:
        st.warning(
            "Nenhum arquivo de teste foi encontrado na pasta "
            "data/sample."
        )

        st.info(
            "Adicione um arquivo PDF ou DOCX fictício à pasta "
            "data/sample para utilizar este modo."
        )

    else:
        selected_file = st.selectbox(
            "Selecione um arquivo de teste",
            options=sample_files,
            format_func=lambda file_path: file_path.name,
        )

        document_to_process = selected_file
        document_name = selected_file.name

        st.caption(
            "Este arquivo já está dentro do ambiente do projeto "
            "e não depende do upload do navegador."
        )

else:
    uploaded_file = st.file_uploader(
        "Selecione um arquivo PDF ou DOCX",
        type=["pdf", "docx"],
    )

    if uploaded_file is not None:
        document_to_process = uploaded_file
        document_name = uploaded_file.name


# =========================================================
# PROCESSAMENTO DO DOCUMENTO
# =========================================================


if document_to_process is not None:
    process_document = st.button(
        "Processar documento",
        type="primary",
    )

    if process_document:
        try:
            with st.spinner(
                "Extraindo, dividindo e indexando o documento..."
            ):
                extracted_sections = load_document(
                    document_to_process
                )

                if not extracted_sections:
                    st.warning(
                        "O documento foi identificado, mas nenhum texto "
                        "pôde ser extraído."
                    )

                    st.session_state.document_processed = False

                else:
                    chunks = create_document_chunks(
                        extracted_sections=extracted_sections,
                        document_name=document_name,
                    )

                    if not chunks:
                        st.warning(
                            "O texto foi extraído, mas nenhum chunk "
                            "válido foi criado."
                        )

                        st.session_state.document_processed = False

                    else:
                        total_indexed = index_chunks(chunks)

                        st.session_state.document_name = document_name
                        st.session_state.document_processed = True
                        st.session_state.total_chunks = total_indexed

                        st.success(
                            "Documento processado com sucesso!"
                        )

        except Exception as error:
            st.session_state.document_processed = False

            st.error(
                f"Não foi possível processar o documento: {error}"
            )


# =========================================================
# CONSULTA AO DOCUMENTO
# =========================================================


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
        "Selecione e processe um documento para liberar "
        "o campo de perguntas."
    )