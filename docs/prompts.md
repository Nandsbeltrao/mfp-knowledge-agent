# Prompts do MFP Knowledge Agent

Este documento registra as instruções utilizadas para gerar as respostas do MFP Knowledge Agent e as melhorias realizadas após a avaliação.

## Objetivos do prompt

O prompt foi desenvolvido para garantir que o agente:

- responda somente com base nos documentos;
- não utilize conhecimento externo;
- não invente nomes, ferramentas, responsáveis, prazos ou valores;
- diferencie respostas completas, parciais e inexistentes;
- indique as fontes utilizadas;
- informe quando não houver evidência suficiente.

## Estrutura enviada à LLM

A chamada utiliza duas mensagens:

1. mensagem de sistema com as regras do agente;
2. mensagem da pessoa usuária com a pergunta e as fontes recuperadas.

### Mensagem da pessoa usuária

```text
Pergunta:
{pergunta}

Fontes recuperadas:
{contexto}
```

### Estrutura de uma fonte

```text
[FONTE 1]
Documento: nome-do-documento.docx
Página: não identificada
Trecho: conteúdo recuperado
```

## Prompt de sistema final

```text
Você é um agente de gestão do conhecimento da Maratona Feminina de Programação.

Responda exclusivamente com base nas fontes fornecidas.

Não utilize conhecimento externo e nunca invente nomes, ferramentas, responsáveis, prazos ou valores.

Antes de responder, classifique internamente a situação como uma das seguintes opções:

1. resposta completa;
2. resposta parcial;
3. ausência total de informação.

Se houver qualquer informação relacionada à pergunta nas fontes, mesmo que incompleta, apresente essa informação e explique claramente qual detalhe não foi especificado.

Por exemplo, se o documento mencionar uma lista de tarefas, mas não informar qual ferramenta organiza essa lista, diga que uma lista de tarefas é exigida, porém a ferramenta não foi especificada.

Não trate esse caso como ausência total de informação.

Use a frase de insuficiência somente quando as fontes não contiverem nenhuma informação relacionada à pergunta.

Nesse caso, responda exatamente:

“Não encontrei informações suficientes nos documentos para responder a essa pergunta.”

Responda em português, de forma clara e objetiva.

Toda afirmação baseada nas fontes deve indicar a referência no formato [Fonte 1], [Fonte 2] ou equivalente.
```

## Comportamentos esperados

### Resposta completa

Quando todas as informações necessárias estão nas fontes, o agente deve responder diretamente e indicar as referências.

Exemplo:

```text
O Departamento de Comunicação é responsável pelas redes sociais, divulgação dos eventos, produção de conteúdo institucional, relacionamento com a comunidade e manutenção do calendário editorial. [Fonte 1]
```

### Resposta parcial

Quando existe informação relacionada, mas algum detalhe não foi especificado, o agente deve apresentar o conteúdo disponível e explicar a limitação.

Exemplo:

```text
O documento informa que cada evento deve possuir uma lista de tarefas, mas não especifica qual ferramenta deve ser utilizada para organizá-la. [Fonte 1]
```

### Ausência total de informação

Quando as fontes não contêm informação relacionada, o agente deve responder:

```text
Não encontrei informações suficientes nos documentos para responder a essa pergunta.
```

## Evolução do prompt

### Versão inicial

A primeira versão instruía a LLM a:

- utilizar somente as fontes;
- não usar conhecimento externo;
- recusar perguntas sem informações suficientes;
- indicar as fontes.

A abordagem funcionou corretamente para perguntas respondíveis e totalmente fora do conteúdo.

### Problema identificado

Durante a avaliação, a seguinte pergunta recebeu uma recusa completa:

```text
Qual ferramenta é utilizada para organizar as tarefas dos eventos?
```

O documento informava que cada evento deveria possuir uma lista de tarefas, mas não especificava a ferramenta utilizada.

A resposta foi segura porque não inventou Trello, Notion, Excel ou outra ferramenta, mas deixou de aproveitar a informação parcial disponível.

### Correção aplicada

O prompt passou a exigir uma classificação interna entre:

1. resposta completa;
2. resposta parcial;
3. ausência total de informação.

Também foi incluído um exemplo específico sobre a diferença entre a existência de uma lista de tarefas e a ausência de uma ferramenta definida.

### Resultado da correção

Após o ajuste, o agente respondeu que:

- uma lista de tarefas era exigida;
- a ferramenta utilizada não havia sido especificada;
- nenhuma ferramenta deveria ser inferida.

O teste foi repetido e aprovado.

## Princípios adotados

### Grounding

As respostas devem estar vinculadas às fontes recuperadas.

### Rastreabilidade

As afirmações devem indicar as referências utilizadas.

### Transparência

O agente deve informar quando um detalhe não está documentado.

### Não alucinação

O agente não deve completar lacunas com suposições ou conhecimento externo.

### Utilidade

A existência de informação parcial não deve provocar uma recusa total quando ainda for possível fornecer uma resposta segura.

## Limitações

Mesmo com um prompt restritivo:

- a LLM pode interpretar uma instrução de forma inesperada;
- o comportamento depende da qualidade da recuperação;
- fontes irrelevantes podem prejudicar a resposta;
- avaliações adicionais são necessárias para documentos maiores;
- prompts não substituem validações técnicas;
- respostas importantes devem ser confirmadas nos documentos de origem.