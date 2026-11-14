import streamlit as st

from src.document_loader import load_document


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

st.subheader("1. Envie um documento")

uploaded_file = st.file_uploader(
    "Selecione um arquivo PDF ou DOCX",
    type=["pdf", "docx"],
)

if uploaded_file is not None:
    try:
        extracted_pages = load_document(uploaded_file)

        if not extracted_pages:
            st.warning(
                "O arquivo foi carregado, mas nenhum texto pôde ser extraído."
            )
        else:
            total_characters = sum(
                len(page["text"])
                for page in extracted_pages
            )

            st.success("Documento processado com sucesso!")

            column_1, column_2, column_3 = st.columns(3)

            column_1.metric(
                "Arquivo",
                uploaded_file.name,
            )

            column_2.metric(
                "Seções extraídas",
                len(extracted_pages),
            )

            column_3.metric(
                "Caracteres",
                total_characters,
            )

            with st.expander("Visualizar texto extraído"):
                for section_number, page in enumerate(
                    extracted_pages,
                    start=1,
                ):
                    if page["page"] is not None:
                        st.markdown(
                            f"### Página {page['page']}"
                        )
                    else:
                        st.markdown(
                            f"### Seção {section_number}"
                        )

                    st.text(page["text"])

    except Exception as error:
        st.error(
            f"Não foi possível processar o documento: {error}"
        )
else:
    st.info(
        "Envie um documento para iniciar o processamento."
    )