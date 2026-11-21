# Decisões técnicas do MFP Knowledge Agent

Este documento registra as principais decisões tomadas durante o desenvolvimento do MFP Knowledge Agent.

## 1. GitHub Codespaces

### Decisão

Utilizar o GitHub Codespaces como ambiente de desenvolvimento.

### Justificativa

A máquina utilizada não possuía Python disponível. O Codespaces permitiu executar Python na nuvem, instalar dependências e trabalhar diretamente no repositório.

### Limitação

O proxy do Codespaces apresentou incompatibilidade com o `st.file_uploader`.

### Tratamento

Foram implementados:

- seleção de documentos da pasta `data/sample`;
- teste automatizado do objeto equivalente ao upload.

---

## 2. Python 3.12

### Decisão

Utilizar Python 3.12 como linguagem principal.

### Justificativa

Python possui um ecossistema consolidado para:

- PDF e DOCX;
- inteligência artificial;
- embeddings;
- bancos vetoriais;
- interfaces de dados;
- testes.

---

## 3. Streamlit

### Decisão

Utilizar Streamlit para a interface do MVP.

### Alternativas consideradas

- React;
- Next.js;
- Vue.js;
- FastAPI com frontend separado.

### Justificativa

Streamlit permitiu criar rapidamente upload, seleção de documentos, perguntas, respostas, métricas e fontes.

### Trade-off

A flexibilidade visual é menor que em uma aplicação construída com frontend separado.

---

## 4. Cohere

### Decisão

Utilizar Cohere para embeddings e geração de respostas.

### Alternativas consideradas

- OpenAI;
- Gemini;
- modelos locais.

### Histórico

A integração inicial com a OpenAI funcionou, mas a conta não possuía créditos de API. Não foi possível gerar uma chave do Gemini no ambiente utilizado.

A Cohere disponibilizou uma chave de avaliação gratuita.

### Limitação

A chave de avaliação não deve ser utilizada em ambiente comercial ou de produção.

---

## 5. ChromaDB

### Decisão

Utilizar ChromaDB em modo local.

### Justificativa

O ChromaDB:

- possui integração simples;
- armazena embeddings e metadados;
- permite busca por similaridade;
- não exige infraestrutura externa;
- atende ao volume do MVP.

### Limitação

O armazenamento local não deve ser tratado como persistência de produção.

---

## 6. RAG sem frameworks adicionais

### Decisão

Implementar o RAG diretamente, sem LangChain ou LlamaIndex.

### Justificativa

A implementação direta permitiu:

- compreender cada etapa;
- reduzir abstrações;
- facilitar o diagnóstico;
- controlar metadados;
- controlar o contexto;
- explicar a arquitetura com clareza.

### Trade-off

A abordagem exige mais código próprio.

---

## 7. Chunking por caracteres

### Decisão

Utilizar:

```text
Tamanho: 1.000 caracteres
Sobreposição: 200 caracteres
```

### Justificativa

A solução é simples, independente de tokenizer e adequada ao MVP.

### Limitação

Caracteres não correspondem diretamente a tokens.

---

## 8. Metadados

### Decisão

Preservar:

```text
identificador
documento
página
número do chunk
texto
```

### Justificativa

Os metadados permitem rastrear as fontes, filtrar documentos e investigar respostas.

### DOCX

A paginação não é preservada porque depende do programa e das configurações de renderização.

---

## 9. Filtro pelo documento ativo

### Decisão

Restringir a recuperação ao documento processado na sessão.

### Justificativa

O filtro evita que chunks de documentos anteriores sejam utilizados indevidamente.

---

## 10. Respostas parciais

### Decisão

Diferenciar:

1. resposta completa;
2. resposta parcial;
3. ausência total.

### Motivo

Uma pergunta sobre ferramentas de organização recebeu inicialmente uma recusa completa, embora o documento mencionasse uma lista de tarefas.

### Correção

O prompt passou a exigir o uso da informação disponível e a indicação explícita do detalhe ausente.

---

## 11. Mensagem de insuficiência

### Decisão

Padronizar a mensagem:

```text
Não encontrei informações suficientes nos documentos para responder a essa pergunta.
```

### Justificativa

A mensagem evita especulação e comunica claramente a limitação documental.

---

## 12. Documento fictício

### Decisão

Criar:

```text
data/sample/mfp_guia_institucional.docx
```

### Justificativa

O documento permite demonstrar o agente sem utilizar dados confidenciais.

### Limitação

O conteúdo é fictício e não representa uma política oficial da MFP.

---

## 13. Segurança da chave

### Decisão

Manter a chave da Cohere fora do código.

### Proteções

O `.gitignore` exclui:

```text
.env
.venv/
chroma_db/
```

A chave não deve aparecer em commits, screenshots ou documentação.

---

## 14. CSS separado

### Decisão

Manter a identidade visual em:

```text
assets/styles.css
```

### Justificativa

A separação mantém o `app.py` focado no funcionamento e permite alterações visuais com menor risco.

---

## 15. Avaliação manual

### Decisão

Avaliar o agente com:

- cinco perguntas respondíveis;
- duas parcialmente respondíveis;
- três não respondíveis.

### Resultado

```text
10 testes executados
10 testes aprovados após o ajuste
0 alucinações identificadas no conjunto avaliado
```

### Limitação

O resultado vale somente para o conjunto analisado e não representa uma métrica estatística geral.

---

## Resumo

As decisões priorizaram:

- funcionamento real;
- IA por API;
- baixo custo;
- transparência;
- segurança;
- rastreabilidade;
- simplicidade arquitetural;
- facilidade de aprendizado;
- possibilidade de evolução.