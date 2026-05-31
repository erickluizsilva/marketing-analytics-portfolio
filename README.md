# Marketing Analytics — Análise de Desempenho de Campanhas e Engajamento de Clientes

> Projeto de portfólio desenvolvido com a metodologia CRISP-DM.  
> Stack: ![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)

---

## Contexto

Um cliente do setor de varejo online enfrenta queda no engajamento e nas taxas de conversão, mesmo com aumento expressivo do investimento em campanhas de marketing. A demanda partiu de dois stakeholders: o gestor de marketing, preocupado com o ROI das campanhas, e o gestor de experiência do cliente, interessado em compreender os padrões de feedback recebido.

Este projeto analisa os dados de campanhas, avaliações e comentários de clientes para identificar os pontos de ruptura na jornada de conversão e propor recomendações acionáveis.

---

## Estrutura do repositório

```
├── data/
│   └── fat_customer_reviews_with_sentiment.csv   # Reviews enriquecidas com análise de sentimento
├── querys.sql                                     # Queries de modelagem dimensional (Star Schema)
├── customer_review_enrichment.py                  # ETL + análise de sentimento (VADER)
└── README.md
```

---

## 1. Business Understanding

**Problema:** apesar do crescimento no investimento em campanhas, o cliente registra declínio simultâneo no engajamento e na conversão — o que sugere desalinhamento entre o público atingido e a proposta de valor comunicada.

**Perguntas analíticas:**
- Em quais etapas do funil os visitantes abandonam a jornada de compra?
- Quais tipos de campanha geram maior engajamento e maior conversão?
- Qual a relação entre o volume de investimento em marketing e o retorno obtido (AOV e conversão)?
- Quais são os principais temas recorrentes no feedback dos clientes — positivos e negativos?

**KPIs acompanhados:**

| KPI | Definição |
|---|---|
| Conversion Rate | % de visitantes que realizaram uma compra |
| Customer Engagement Rate | Nível de interação com conteúdos (cliques, curtidas, comentários) |
| Average Order Value (AOV) | Valor médio por transação |
| Customer Feedback Score | Média das avaliações dos clientes |

---

## 2. Data Understanding

Quatro tabelas foram utilizadas, todas armazenadas no banco `PortfolioProject_MarketingAnalytics` no SQL Server local:

| Tabela | Descrição |
|---|---|
| `dbo.products` | Catálogo de produtos com preço |
| `dbo.customers` | Cadastro de clientes |
| `dbo.geography` | Localização geográfica (país e cidade) |
| `dbo.customer_reviews` | Avaliações textuais e notas dos clientes |
| `dbo.engagement_data` | Métricas de engajamento por conteúdo e campanha (views, cliques, curtidas) |
| `dbo.customer_journey` | Etapas da jornada de compra por cliente e produto |

A análise exploratória investigou distribuições, correlações entre variáveis e qualidade dos dados (valores ausentes, duplicatas, inconsistências de tipo).

---

## 3. Data Preparation

### Modelagem dimensional — [`querys.sql`](querys.sql)

As queries constroem as dimensões do Star Schema diretamente no SQL Server:

| Tabela | Tipo | Transformações aplicadas |
|---|---|---|
| `dim_products` | Dimensão | Categorização de faixa de preço (`Low / Medium / High`) |
| `dim_customers` | Dimensão | Join com `geography` para enriquecer com país e cidade |
| `fat_customer_reviews` | Fato | Remoção de espaços duplos no campo `ReviewText` |
| `fat_engagement_data` | Fato | Normalização de `ContentType` (padronização para maiúsculas + substituição de `SocialMedia`), separação de `ViewsClicksCombined` em colunas `Views` e `Clicks` via `SUBSTRING`/`CHARINDEX`, exclusão de registros do tipo `Newsletter` |
| `fat_customer_journey` | Fato | Deduplicação por `ROW_NUMBER`, imputação de `Duration` com média da data via `AVG() OVER` |

### Análise de sentimento — [`customer_review_enrichment.py`](customer_review_enrichment.py)

- Conexão com SQL Server via `SQLAlchemy` + `pyodbc` (autenticação Windows)
- Aplicação do modelo **VADER** (NLTK) sobre o campo `ReviewText`
- Geração de três colunas derivadas:

| Coluna | Descrição |
|---|---|
| `SentimentScore` | Score composto VADER (−1 a 1) |
| `SentimentCategory` | Categoria cruzando score textual e nota numérica (`Positive`, `Negative`, `Mixed Positive`, `Mixed Negative`, `Neutral`) |
| `SentimentBucket` | Faixa do score (`-1.0 to -0.5`, `-0.49 to 0.0`, `0.0 to 0.49`, `0.5 to 1.0`) |

- Saída exportada para [`data/fat_customer_reviews_with_sentiment.csv`](data/fat_customer_reviews_with_sentiment.csv)

---

## 4. Modeling

Três análises centrais foram conduzidas:

**Funil de conversão:** identificação das etapas com maior taxa de abandono, segmentadas por campanha e canal de aquisição.

**Segmentação de clientes:** agrupamento por nível de engajamento, identificando perfis de alto e baixo valor para o negócio.

**Correlação investimento × retorno:** análise da relação entre gasto em campanhas e métricas de conversão e AOV ao longo do tempo.

---

## 5. Evaluation

**Principais achados:**

- _[a preencher após a análise]_
- _[a preencher após a análise]_
- _[a preencher após a análise]_

As perguntas definidas na fase 1 foram respondidas integralmente. Os achados indicam [síntese da conclusão principal], com implicações diretas sobre [ação recomendada ao cliente].

---

## 6. Deployment

| Entregável | Link |
|---|---|
| Dashboard Power BI | [Acessar]() |
| Script SQL (dimensões) | [`querys.sql`](querys.sql) |
| Script Python (sentimento) | [`customer_review_enrichment.py`](customer_review_enrichment.py) |
| Reviews enriquecidas | [`fat_customer_reviews_with_sentiment.csv`](data/fat_customer_reviews_with_sentiment.csv) |

---

## Limitações

- Os dados utilizados são simulados para fins de portfólio — nenhum dado real de clientes foi exposto
- A análise de sentimento (VADER) foi calibrada para textos em inglês; resultados podem variar com textos multilíngues
- Análises de correlação entre investimento e retorno assumem causalidade apenas como hipótese — não há controle de variáveis confundidoras

---

## Sobre o projeto

Desenvolvido por [Erick Silva](https://linkedin.com/in/) como projeto de portfólio para a posição de Analista de Dados.  
Metodologia: CRISP-DM | Período: 2026
