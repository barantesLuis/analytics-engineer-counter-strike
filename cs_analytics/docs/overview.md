# CS Analytics

## Sobre o projeto

Projeto de Analytics Engineering desenvolvido para análise
de dados competitivos de Counter-Strike.

O projeto realiza ingestão de dados provenientes de uma API
externa, tratamento e padronização dos dados utilizando dbt
e DuckDB, e construção de modelos analíticos para consumo.

## Arquitetura

O projeto é organizado em três camadas:

### Bronze

Dados brutos provenientes da API, preservando a estrutura
original da fonte.

### Silver

Dados tratados e padronizados, com estruturas aninhadas
normalizadas e nomes de colunas orientados ao contexto analítico.

### Gold

Modelos finais orientados às perguntas de negócio e consumo
analítico.

## Tecnologias

- Python
- API REST
- DuckDB
- dbt
- SQL
- Terraform