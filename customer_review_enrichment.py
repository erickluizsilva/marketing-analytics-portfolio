
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

# Baixa o léxico do VADER caso ainda não esteja disponível localmente
nltk.download('vader_lexicon')

def fetch_data_from_sql():
    # Conecta ao SQL Server local via autenticação Windows e retorna as avaliações dos clientes
    SERVER_NAME = "localhost"
    DATABASE_NAME = "PortfolioProject_MarketingAnalytics"

    engine = create_engine(
        f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}"
        "?trusted_connection=yes"
        "&driver=ODBC+Driver+17+for+SQL+Server"
    )

    query = """
    SELECT
        ReviewID,
        CustomerID,
        ProductID,
        ReviewDate,
        Rating,
        REPLACE(ReviewText,'  ',' ') AS ReviewText
    FROM
        dbo.customer_reviews;

    """

    df = pd.read_sql(query, engine)

    return df

# Busca os dados de avaliações diretamente do banco
customer_reviews_df = fetch_data_from_sql()

# Instancia o analisador de sentimento VADER
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    # Retorna o score composto do VADER (varia de -1 a 1)
    sentiment = sia.polarity_scores(review)
    return sentiment['compound']

def categorize_sentiment(score, rating):
    # Determina a categoria de sentimento cruzando o score textual com a nota numérica
    if score > 0.05:  # Score positivo
        if rating >= 4:
            return 'Positive'       # Nota alta e sentimento positivo
        elif rating == 3:
            return 'Mixed Positive' # Nota neutra, mas sentimento positivo
        else:
            return 'Mixed Negative' # Nota baixa, mas sentimento positivo
    elif score < -0.05:  # Score negativo
        if rating <= 2:
            return 'Negative'       # Nota baixa e sentimento negativo
        elif rating == 3:
            return 'Mixed Negative' # Nota neutra, mas sentimento negativo
        else:
            return 'Mixed Positive' # Nota alta, mas sentimento negativo
    else:  # Score neutro
        if rating >= 4:
            return 'Positive'  # Nota alta com sentimento neutro
        elif rating <= 2:
            return 'Negative'  # Nota baixa com sentimento neutro
        else:
            return 'Neutral'   # Nota neutra e sentimento neutro

def sentiment_bucket(score):
    # Agrupa o score em faixas para facilitar a visualização no dashboard
    if score >= 0.5:
        return '0.5 to 1.0'    # Sentimento fortemente positivo
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'   # Sentimento levemente positivo
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Sentimento levemente negativo
    else:
        return '-1.0 to -0.5'  # Sentimento fortemente negativo

# Calcula o score de sentimento para cada avaliação
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Categoriza o sentimento combinando score textual e nota numérica
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Classifica o score em faixas predefinidas
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Exibe as primeiras linhas para validação rápida
print(customer_reviews_df.head())

# Exporta o DataFrame enriquecido com as colunas de sentimento
customer_reviews_df.to_csv('data/fat_customer_reviews_with_sentiment.csv', index=False)
