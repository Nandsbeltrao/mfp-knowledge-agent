# Arquitetura do MFP Knowledge Agent

## Visão geral

O MFP Knowledge Agent utiliza uma arquitetura de Retrieval-Augmented Generation, ou RAG, para responder perguntas com base no conteúdo de documentos PDF e DOCX.

A solução separa a interface, o processamento dos documentos, a geração de embeddings, a recuperação semântica e a geração das respostas.

## Fluxo principal

```text
Documento PDF ou DOCX
        ↓
Extração do texto
        ↓
Normalização do conteúdo
        ↓
Divisão em chunks com sobreposição
        ↓
Geração de embeddings com a Cohere
        ↓
Armazenamento no ChromaDB
        ↓
Pergunta da pessoa usuária
        ↓
Embedding da pergunta
        ↓
Busca semântica
        ↓
Recuperação dos trechos relevantes
        ↓
Envio do contexto para a LLM
        ↓
Resposta fundamentada + fontes
```

## Componentes

### Interface

**Arquivo:** `app.py`

Responsável por:

- exibir a interface em Streamlit;
- receber a chave da Cohere durante a sessão;
- permitir a seleção de documentos demonstrativos;
- receber arquivos PDF e DOCX;
- iniciar o processamento;
- receber perguntas;
- apresentar as respostas;
- exibir as fontes recuperadas;
- controlar o estado da sessão.

### Carregamento de documentos

**Arquivo:** `src/document_loader.py`

Responsável por:

- identificar o formato do documento;
- extrair texto de arquivos PDF;
- preservar o número das páginas dos PDFs;
- extrair os parágrafos de arquivos DOCX;
- rejeitar formatos não suportados;
- retornar somente seções com conteúdo válido.

### Divisão do texto

**Arquivo:** `src/text_splitter.py`

Responsável por:

- normalizar espaços e quebras de linha;
- dividir o conteúdo em chunks;
- aplicar sobreposição entre chunks;
- preservar os metadados do documento;
- criar identificadores para cada chunk.

Configuração utilizada no MVP:

```text
Tamanho do chunk: 1.000 caracteres
Sobreposição: 200 caracteres
```

### Embeddings

**Arquivo:** `src/embeddings.py`

Responsável por:

- carregar a chave da Cohere;
- criar o cliente da API;
- gerar embeddings para os documentos;
- gerar embeddings para as perguntas;
- diferenciar `search_document` e `search_query`;
- rejeitar entradas vazias.

### Banco vetorial

**Arquivo:** `src/vector_store.py`

Responsável por:

- criar a coleção no ChromaDB;
- armazenar textos, embeddings e metadados;
- atualizar chunks com o mesmo identificador;
- executar buscas por similaridade;
- filtrar a consulta pelo documento ativo;
- retornar os trechos, fontes e distâncias vetoriais.

### Geração das respostas

**Arquivo:** `src/generator.py`

Responsável por:

- organizar os trechos recuperados;
- construir o contexto enviado à LLM;
- aplicar regras de grounding;
- diferenciar respostas completas, parciais e inexistentes;
- impedir o uso de conhecimento externo;
- retornar respostas com referências às fontes.

## Estrutura dos chunks

Cada chunk possui a seguinte estrutura:

```python
{
    "id": "nome-do-documento-1",
    "document": "nome-do-documento.pdf",
    "page": 1,
    "chunk_number": 1,
    "text": "Conteúdo do trecho"
}
```

Esses metadados permitem rastrear a origem das informações utilizadas nas respostas.

## Fluxo de indexação

```text
Arquivo
  ↓
load_document()
  ↓
Lista de seções extraídas
  ↓
create_document_chunks()
  ↓
Lista de chunks com metadados
  ↓
generate_embeddings(input_type="search_document")
  ↓
index_chunks()
  ↓
ChromaDB
```

## Fluxo de consulta

```text
Pergunta
  ↓
generate_embeddings(input_type="search_query")
  ↓
Busca por similaridade no ChromaDB
  ↓
Filtro pelo documento ativo
  ↓
Trechos mais relevantes
  ↓
build_context()
  ↓
Cohere Chat API
  ↓
Resposta com indicação das fontes
```

## Grounding

A resposta é controlada por quatro mecanismos:

1. Recuperação semântica dos trechos mais relacionados à pergunta.
2. Inclusão de metadados sobre documento, página e chunk.
3. Prompt que restringe a resposta às fontes recuperadas.
4. Mensagem padronizada quando nenhuma informação relacionada está disponível.

## Tratamento de respostas parciais

O agente diferencia três situações:

1. **Resposta completa:** todas as informações necessárias estão disponíveis.
2. **Resposta parcial:** existe informação útil, mas algum detalhe não está documentado.
3. **Ausência total:** não existe informação relacionada à pergunta.

Nas respostas parciais, o agente apresenta o que está documentado e informa explicitamente qual detalhe não foi especificado.

## Segurança

- A chave da API não é armazenada no código.
- O arquivo `.env` não é versionado.
- O banco vetorial local não é enviado ao GitHub.
- Os documentos demonstrativos contêm dados fictícios.
- Documentos confidenciais não devem ser usados sem autorização.

## Limitações arquiteturais

- O MVP utiliza um documento ativo por vez.
- O ChromaDB é executado localmente.
- O armazenamento pode ser perdido em ambientes efêmeros.
- A aplicação ainda não possui autenticação.
- Não existe controle de acesso por departamento.
- PDFs formados exclusivamente por imagens exigem OCR.
- O processamento não utiliza filas ou tarefas assíncronas.
- O upload apresentou incompatibilidade com o proxy do GitHub Codespaces.

## Evolução para produção

Uma arquitetura de produção poderia incluir:

- frontend separado;
- API em FastAPI;
- autenticação;
- armazenamento seguro de arquivos;
- banco vetorial gerenciado;
- controle de acesso por área;
- processamento assíncrono;
- logs estruturados;
- monitoramento de custos;
- observabilidade;
- avaliação automatizada;
- integração com SharePoint ou Google Drive.