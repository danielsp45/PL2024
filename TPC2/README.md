# TPC2: Conversor de Markdown para HTML

## 2024-03-03

## Autor:

- a100545
- Daniel da Silva Pereira

## Resumo

O objetivo deste trabaho centra-se na criação de um conversor de ficheiros Markdown em ficheiros HTML, mantendo sempre toda a semântica existente.

Para tal, fez-se proveito de expressões regulares (RegEx) de modo a identificar padrões do formato Markdown. A linguagem Python possui a biblioteca re, que suporta a manipulação dessas ditas expressões.

Foram apenas trabalhados os seguintes padrões:

Títulos: # This is a title, ## This is a subtitle, etc
Negrito: **This is bold**, __This is bold__
Itálico: *This is in italics*, _This is in italics_
Listas: - This is an unordered list element, 1. This is an ordered list element
Imagens: ![This is an image title](This is an image URL)
Links: [This is a link text](This is a link URL)
