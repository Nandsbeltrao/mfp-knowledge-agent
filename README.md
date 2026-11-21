# ⭐ MFP Knowledge Agent

Agente inteligente para consulta e preservação do conhecimento institucional da **Maratona Feminina de Programação (MFP)**.

O projeto utiliza **Retrieval-Augmented Generation (RAG)** para permitir que pessoas façam perguntas em linguagem natural e recebam respostas fundamentadas nos documentos processados, acompanhadas das fontes utilizadas.

> **Status:** MVP funcional, avaliado e documentado.

---

## Sobre o projeto

Organizações formadas por diferentes departamentos, coordenações e pessoas voluntárias frequentemente armazenam informações importantes em documentos, arquivos e registros de gestões anteriores.

Essa fragmentação pode dificultar:

- a localização rápida de informações;
- o entendimento dos processos internos;
- a consulta às responsabilidades dos departamentos;
- a integração de novas integrantes;
- a preservação do conhecimento institucional;
- a continuidade entre diferentes gestões;
- a redução de retrabalho.

O **MFP Knowledge Agent** foi desenvolvido para transformar documentos institucionais em uma base de conhecimento pesquisável.

Após o processamento de um documento, a pessoa usuária pode fazer perguntas em linguagem natural e receber uma resposta elaborada exclusivamente a partir das informações encontradas no conteúdo enviado.

---

## Objetivo

Demonstrar como inteligência artificial generativa pode ser aplicada a um problema real de gestão do conhecimento, combinando:

- processamento de documentos;
- embeddings;
- busca semântica;
- banco vetorial;
- recuperação de contexto;
- integração com uma LLM;
- rastreabilidade das fontes;
- controle de respostas sem evidência;
- interface funcional.

O projeto também foi construído para demonstrar competências relacionadas à atuação de uma pessoa **AI Builder**, incluindo integração de tecnologias, engenharia de prompts, avaliação de respostas e tradução de uma necessidade de negócio em uma solução funcional.

---

## Funcionalidades

### Processamento documental

- Leitura de arquivos PDF.
- Leitura de arquivos DOCX.
- Extração do conteúdo textual.
- Preservação do número das páginas dos arquivos PDF.
- Validação de documentos sem conteúdo extraível.

### Pipeline de RAG

- Normalização do texto extraído.
- Divisão do conteúdo em chunks.
- Sobreposição entre chunks para preservação de contexto.
- Geração de embeddings reais pela Cohere API.
- Armazenamento dos vetores no ChromaDB.
- Busca semântica baseada na pergunta realizada.
- Recuperação dos trechos mais relevantes.

### Geração das respostas

- Integração com uma LLM real da Cohere.
- Respostas elaboradas somente a partir dos trechos recuperados.
- Indicação das fontes utilizadas.
- Identificação do documento e da página, quando disponível.
- Exibição dos trechos recuperados.
- Tratamento de informações parcialmente disponíveis.
- Recusa de perguntas sem evidência documental.
- Prevenção de nomes, prazos, ferramentas ou valores inventados.

### Interface

- Interface construída em Streamlit.
- Modo de upload de arquivos PDF e DOCX.
- Documento fictício disponível para demonstração.
- Indicadores de documento ativo e quantidade de chunks.
- Campo de perguntas.
- Visualização das fontes recuperadas.
- Identidade visual inspirada na MFP.

---

## Como funciona

O fluxo principal da aplicação é:

```text
Documento PDF ou DOCX
        ↓
Extração do texto
        ↓
Normalização do conteúdo
        ↓
Divisão em chunks com sobreposição
        ↓
Geração de embeddings com Cohere
        ↓
Armazenamento no ChromaDB
        ↓
Pergunta da pessoa usuária
        ↓
Geração do embedding da pergunta
        ↓
Busca semântica por similaridade
        ↓
Recuperação dos trechos mais relevantes
        ↓
Envio do contexto para a LLM
        ↓
Resposta fundamentada + fontes
```

---

## Arquitetura

A aplicação foi organizada em componentes independentes para separar a interface, o processamento documental e o pipeline de inteligência artificial.

```text
┌──────────────────────────────┐
│      Interface Streamlit     │
│            app.py            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Carregador de documentos │
│    PDF e DOCX → conteúdo     │
│    src/document_loader.py    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Divisão em chunks        │
│  texto + metadados + overlap │
│    src/text_splitter.py      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Cohere Embeddings       │
│ documentos e perguntas      │
│      src/embeddings.py       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          ChromaDB            │
│ armazenamento e recuperação  │
│     src/vector_store.py      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Cohere Chat API        │
│ resposta baseada no contexto │
│       src/generator.py       │
└──────────────────────────────┘
```

---

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python 3.12 | Linguagem principal |
| Streamlit | Interface da aplicação |
| Cohere API | Embeddings e geração das respostas |
| ChromaDB | Banco vetorial local |
| PyPDF | Extração de texto de PDFs |
| python-docx | Leitura de documentos DOCX |
| python-dotenv | Gerenciamento das variáveis de ambiente |
| Git | Controle de versão |
| GitHub | Hospedagem e documentação do código |
| GitHub Codespaces | Ambiente de desenvolvimento em nuvem |

---

## Decisões técnicas

### Python

Python foi escolhido pelo ecossistema consolidado para processamento documental, inteligência artificial, bancos vetoriais e construção rápida de protótipos.

### Streamlit

Streamlit foi escolhido para acelerar a criação de uma interface funcional e permitir que o foco do desenvolvimento permanecesse no pipeline de inteligência artificial.

A decisão evitou a necessidade de criar e integrar separadamente frontend, backend e comunicação entre APIs durante o MVP.

### Cohere

A Cohere foi utilizada para:

- gerar embeddings dos documentos;
- gerar embeddings das perguntas;
- produzir respostas em linguagem natural;
- executar chamadas reais de inteligência artificial.

A chave de avaliação foi utilizada exclusivamente para desenvolvimento e demonstração do projeto.

### ChromaDB

O ChromaDB foi escolhido como banco vetorial devido à simplicidade de integração, execução local e adequação a um MVP com um volume reduzido de documentos.

### Implementação direta do RAG

O pipeline foi construído diretamente, sem LangChain ou LlamaIndex.

Essa escolha teve como objetivos:

- reduzir abstrações desnecessárias;
- facilitar o entendimento de cada etapa;
- tornar o fluxo de dados visível;
- permitir maior controle sobre embeddings, recuperação e prompts;
- simplificar a identificação de erros.

---

## Estrutura do repositório

```text
mfp-knowledge-agent/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── styles.css
│   └── Images/
├── data/
│   └── sample/
│       └── mfp_guia_institucional.docx
├── evaluation/
│   ├── questions.json
│   └── results.json
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── generator.py
└── tests/
    ├── __init__.py
    └── test_document_upload.py
```

### Responsabilidade dos principais arquivos

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Interface Streamlit e controle do fluxo da aplicação |
| `document_loader.py` | Extração de texto de PDF e DOCX |
| `text_splitter.py` | Divisão dos textos em chunks com metadados |
| `embeddings.py` | Integração com os embeddings da Cohere |
| `vector_store.py` | Indexação e busca semântica no ChromaDB |
| `generator.py` | Construção do contexto, prompt e resposta final |
| `styles.css` | Identidade visual da interface |
| `questions.json` | Perguntas utilizadas na avaliação |
| `results.json` | Resultados reais obtidos na avaliação |
| `test_document_upload.py` | Teste do processamento de arquivos equivalentes ao upload |

---

## Requisitos

Antes de executar o projeto, é necessário ter:

- Python 3.12;
- Git;
- uma chave de avaliação da Cohere;
- acesso a um terminal.

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Nandsbeltrao/mfp-knowledge-agent.git
```

Acesse a pasta:

```bash
cd mfp-knowledge-agent
```

### 2. Criar o ambiente virtual

```bash
python3.12 -m venv .venv
```

### 3. Ativar o ambiente virtual

#### Linux ou macOS

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Atualizar o pip

```bash
python -m pip install --upgrade pip
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto.

```env
COHERE_API_KEY=sua_chave_aqui
COHERE_EMBEDDING_MODEL=embed-v5.0-fast
COHERE_CHAT_MODEL=command-a-plus-05-2026
```

A aplicação também permite informar uma chave de avaliação da Cohere durante a sessão por meio da barra lateral.

> Nunca publique o arquivo `.env` ou uma chave real no GitHub.

### 7. Executar a aplicação

```bash
streamlit run app.py
```

Por padrão, a aplicação estará disponível em:

```text
http://localhost:8501
```

Em ambientes remotos, pode ser necessário encaminhar a porta utilizada pelo Streamlit.

---

## Documento demonstrativo

O repositório contém um documento fictício criado exclusivamente para demonstração:

```text
data/sample/mfp_guia_institucional.docx
```

O documento contém exemplos fictícios de:

- objetivo da organização;
- responsabilidades do Departamento de Comunicação;
- responsabilidades do Departamento de Tecnologia;
- integração de novas integrantes;
- organização de eventos;
- cuidados com dados.

O conteúdo não deve ser interpretado como política oficial da MFP.

---

## Exemplos de uso

### Pergunta respondível

```text
Quais são as responsabilidades do Departamento de Comunicação?
```

Comportamento esperado:

- informar as responsabilidades descritas no documento;
- indicar a fonte utilizada;
- permitir a visualização do trecho recuperado.

### Pergunta parcialmente respondível

```text
Qual ferramenta é utilizada para organizar as tarefas dos eventos?
```

Comportamento esperado:

- informar que o documento exige uma lista de tarefas;
- esclarecer que nenhuma ferramenta específica foi informada;
- não inventar Trello, Notion, Excel, Planner ou outra ferramenta.

### Pergunta não respondível

```text
Qual é o orçamento anual da organização?
```

Comportamento esperado:

```text
Não encontrei informações suficientes nos documentos para responder a essa pergunta.
```

---

## Estratégia de grounding

O projeto adota diferentes mecanismos para reduzir respostas sem fundamento.

### Prompt restritivo

A LLM recebe instruções para:

- utilizar exclusivamente as fontes recuperadas;
- não usar conhecimento externo;
- não inventar nomes, ferramentas, responsáveis, prazos ou valores;
- diferenciar informação completa, parcial e inexistente;
- indicar as fontes utilizadas.

### Recuperação semântica

A pergunta é transformada em embedding e comparada aos chunks armazenados no ChromaDB.

Os trechos mais próximos semanticamente são enviados à LLM como contexto.

### Metadados

Cada chunk armazena:

```text
documento
página
número do chunk
texto
```

### Resposta de insuficiência

Quando nenhuma informação relacionada é encontrada, o agente responde:

```text
Não encontrei informações suficientes nos documentos para responder a essa pergunta.
```

### Informações parciais

Quando existe informação relacionada, mas incompleta, o agente apresenta o que está documentado e explica qual detalhe não foi informado.

---

## Avaliação

O agente foi avaliado manualmente com dez perguntas divididas em três categorias.

| Categoria | Quantidade | Resultado final |
|---|---:|---:|
| Respondíveis | 5 | 5 aprovadas |
| Parcialmente respondíveis | 2 | 2 aprovadas |
| Não respondíveis | 3 | 3 aprovadas |
| **Total** | **10** | **10 aprovadas** |

### Critérios utilizados

Cada resposta foi verificada considerando:

- aderência ao conteúdo do documento;
- indicação da fonte;
- compatibilidade entre a resposta e o trecho recuperado;
- ausência de informações inventadas;
- recusa adequada quando não havia evidência;
- tratamento adequado de informações parciais.

### Resultado

No conjunto avaliado:

- 10 testes foram executados;
- 10 testes foram aprovados após o ajuste final;
- nenhuma alucinação foi identificada;
- todas as perguntas não respondíveis foram recusadas corretamente.

### Melhoria identificada durante a avaliação

Inicialmente, uma pergunta parcialmente respondível recebeu uma recusa completa.

A pergunta foi:

```text
Qual ferramenta é utilizada para organizar as tarefas dos eventos?
```

O documento informava a necessidade de uma lista de tarefas, mas não especificava a ferramenta utilizada.

O prompt foi ajustado para diferenciar:

1. resposta completa;
2. resposta parcial;
3. ausência total de informação.

Após o ajuste, o agente passou a responder que uma lista de tarefas é exigida, mas que a ferramenta não foi especificada.

Os detalhes da avaliação estão disponíveis em:

```text
evaluation/questions.json
evaluation/results.json
```

---

## Teste de processamento do upload

O projeto contém um teste que simula o objeto entregue pelo uploader do Streamlit.

Para executar:

```bash
PYTHONPATH=. python tests/test_document_upload.py
```

O teste verifica:

- processamento de arquivo DOCX;
- processamento de arquivo PDF;
- preservação do nome do arquivo;
- extração do texto;
- preservação da página do PDF;
- compatibilidade do carregador com arquivos mantidos em memória.

---

## Segurança e privacidade

Foram adotados os seguintes cuidados:

- a chave da API não é armazenada no código;
- o arquivo `.env` está protegido pelo `.gitignore`;
- o ambiente virtual não é enviado ao GitHub;
- o banco vetorial local não é versionado;
- os documentos demonstrativos contêm dados fictícios;
- documentos internos não devem ser publicados em repositórios públicos;
- dados pessoais não devem ser usados sem autorização;
- testes devem utilizar dados fictícios, anonimizados ou autorizados.

A chave de avaliação da Cohere é destinada apenas a desenvolvimento e demonstração, não a uso comercial ou produção.

---

## Limitações conhecidas

- Arquivos DOCX não preservam paginação confiável, pois a divisão em páginas depende do programa e das configurações utilizadas para renderização.
- PDFs compostos somente por imagens precisam de uma etapa adicional de OCR.
- A avaliação atual utiliza apenas um documento fictício.
- O conjunto de dez perguntas é pequeno e não representa uma métrica estatística de precisão.
- A qualidade da recuperação pode variar conforme o tamanho, a clareza e a estrutura dos documentos.
- O ChromaDB está configurado para armazenamento local.
- O armazenamento local não deve ser tratado como solução persistente para produção.
- A aplicação ainda não possui autenticação ou controle de permissões.
- A aplicação processa um documento ativo por vez.
- O upload pelo navegador apresentou incompatibilidade com o proxy do GitHub Codespaces.
- O processamento de objetos equivalentes ao upload foi validado por teste automatizado.
- O uso da aplicação depende dos limites da chave da Cohere.

---

## Possíveis evoluções

- Processamento simultâneo de vários documentos.
- Organização dos documentos por departamento.
- Filtros por categoria, área ou data.
- Identificação de documentos desatualizados.
- Comparação entre documentos e versões.
- Identificação de lacunas na documentação.
- OCR para PDFs digitalizados.
- Histórico de conversas.
- Autenticação de pessoas usuárias.
- Controle de acesso por área.
- Persistência em banco vetorial gerenciado.
- Integração com Google Drive.
- Integração com SharePoint.
- Integração com outras fontes institucionais.
- Monitoramento de custos e utilização.
- Avaliação automatizada com conjunto maior de perguntas.
- Coleta estruturada de feedback sobre as respostas.
- Suporte a outros provedores de LLM.

---

## Aprendizados

O desenvolvimento do projeto envolveu:

- configuração de um ambiente Python em nuvem;
- tratamento seguro de chaves de API;
- processamento de arquivos PDF e DOCX;
- criação de chunks com sobreposição;
- integração com uma API de embeddings;
- implementação de busca semântica;
- utilização de banco vetorial;
- criação de prompts orientados a grounding;
- tratamento de respostas parciais;
- elaboração de testes de avaliação;
- documentação de limitações;
- construção de uma interface funcional;
- versionamento incremental com Git e GitHub.

---

## Status do projeto

### MVP técnico

- [x] Processamento de PDF.
- [x] Processamento de DOCX.
- [x] Chunking.
- [x] Embeddings reais.
- [x] Banco vetorial.
- [x] Busca semântica.
- [x] Integração com LLM real.
- [x] Respostas com fontes.
- [x] Tratamento de informações parciais.
- [x] Recusa quando não há evidência.
- [x] Interface funcional.
- [x] Documento demonstrativo.
- [x] Avaliação manual.
- [x] Teste automatizado do processamento de upload.
- [x] Identidade visual separada da lógica da aplicação.

### Próximas entregas

- [ ] Publicação em um ambiente acessível externamente.
- [ ] Validação final do upload fora do proxy do Codespaces.
- [ ] Vídeo de demonstração.
- [ ] Ampliação do conjunto de avaliação.

---

## Autora

Desenvolvido por **Fernanda Leite** como projeto de portfólio para demonstrar a aplicação de inteligência artificial generativa na resolução de um problema real de gestão do conhecimento.

O projeto foi inspirado em necessidades observadas na experiência de comunicação, organização de processos e gestão de projetos na Maratona Feminina de Programação.

---

## Aviso

Este é um projeto de demonstração e portfólio.

O documento institucional incluído no repositório contém informações fictícias, criadas exclusivamente para testar o comportamento da aplicação.

A utilização do código em ambientes reais exige revisão de segurança, privacidade, persistência, autenticação, controle de acesso e conformidade com as políticas da organização.