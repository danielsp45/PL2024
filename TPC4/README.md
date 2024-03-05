# TPC4: Analisador léxico

## 2024-03-05

## Autor:

- a100545
- Daniel da Silva Pereira

## Resumo

O principal objetivo deste programa é a criação de um analisador léxico que consiga identificar e classificar os tokens de uma expressão SQL.

Para tal, o programa deverá ser capaz de identificar os seguintes tokens:

Comandos mais comuns: SELECT, INSERT INTO, UPDATE, DELETE FROM, CREATE TABLE, DROP TABLE, ALTER TABLE
Fields: *
Números: inteiros e decimais
Delimitadores: (, ), ,
Delimitador final: ;
Operadores matemáticos: =, <>, !=, >, <, >=, <=, +, -, *, /
Operadores SQL mais comuns: AND, OR, NOT, LIKE, IN
Recorreu-se à biblioteca ply, que é uma ferramenta para a construção de analisadores léxicos e sintáticos.
