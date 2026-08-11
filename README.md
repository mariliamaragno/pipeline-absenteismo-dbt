# Análise de Absenteísmo — Pipeline de Engenharia de Dados

Projeto de portfólio que constrói um pipeline completo de dados sobre absenteísmo no trabalho, combinando engenharia de dados, modelagem analítica e governança de qualidade.

## Objetivo

Transformar dados brutos de ausências no trabalho em métricas confiáveis e testadas, aplicando princípios de rotina de gestão e melhoria contínua (PDCA) à própria arquitetura de dados.

## Stack

- **Postgres** — banco de dados (rodando via Docker)
- **dbt** — transformação, testes de qualidade e documentação
- **Python (pandas, sqlalchemy)** — carga inicial do dado bruto
- **Docker** — ambiente containerizado
- *(em construção)* **Airflow** — orquestração do pipeline

## Fonte dos dados

Dataset público ["Absenteeism at Work"](https://archive.ics.uci.edu/dataset/445/absenteeism+at+work), UCI Machine Learning Repository — 740 registros de ausências, incluindo motivo (classificado por CID), dia da semana, distância até o trabalho, carga de dependentes, entre outras variáveis.

## Arquitetura

O projeto segue uma arquitetura em camadas dentro do dbt:

- **staging** — limpeza e padronização do dado bruto (renomeação de colunas, tratamento de nomes com espaços/inconsistências do CSV original)
- **seed** — tabela de-para dos motivos de ausência (`reason_codes.csv`), construída manualmente a partir da classificação CID, já que o dataset original só traz códigos numéricos
- **intermediate** — enriquecimento: junta staging e seed, traduz códigos de dia da semana
- **marts** — métricas finais de negócio: absenteísmo por dia da semana e por motivo

## Qualidade de dados

7 testes automatizados no dbt cobrindo:
- Valores nulos em colunas críticas (`not_null`)
- Valores aceitos dentro de listas válidas (`accepted_values`)
- Faixas plausíveis para variáveis numéricas (`accepted_range`, via `dbt_utils`)

Todos os testes passam atualmente, confirmando a integridade do dado nessas dimensões.

## Principais achados (preliminares)

- **Segunda-feira** concentra o maior volume de ausências (161 ocorrências, 1.489 horas totais) e a maior média de horas por ausência (9,25h) — consistente com padrões conhecidos de absenteísmo pós-fim de semana.

## Como rodar localmente

\`\`\`bash
# 1. Subir o Postgres
docker run -d --name absenteeismo-pg \\
  -e POSTGRES_USER=dbt_user -e POSTGRES_PASSWORD=dbt_pass \\
  -e POSTGRES_DB=absenteeismo -p 5433:5432 postgres:16

# 2. Ambiente Python
python3 -m venv venv && source venv/bin/activate
pip install dbt-postgres pandas sqlalchemy psycopg2-binary

# 3. Carregar o dado bruto
python load_raw.py

# 4. Rodar o dbt
cd absenteismo_dbt
dbt deps
dbt seed
dbt run
dbt test
\`\`\`

> **Nota sobre credenciais:** as credenciais usadas neste projeto (\`dbt_user\`/\`dbt_pass\`) são propositalmente simples por se tratar de um ambiente de estudo local. Em produção, senhas seriam geradas de forma segura e geridas via variáveis de ambiente ou um gerenciador de segredos (ex: AWS Secrets Manager).

## Roadmap

- [x] Modelagem em camadas (staging → intermediate → marts)
- [x] Seed de enriquecimento (motivos de ausência)
- [x] Testes de qualidade de dados
- [ ] Orquestração via Airflow
- [ ] Análise de sazonalidade em Python (segunda-feira, véspera de feriado)
- [ ] Documentação gerada via \`dbt docs\`

---

Projeto desenvolvido por [Marília Maragno](https://www.linkedin.com/in/mariliamaragno/) como parte de estudo aplicado em engenharia de dados.
