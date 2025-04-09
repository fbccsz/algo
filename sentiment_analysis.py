from textblob import TextBlob
import pandas as pd

def analisar_sentimento(texto):
    blob = TextBlob(texto)
    polaridade = blob.sentiment.polarity

    if polaridade > 0.1:
        return 'Positivo'
    elif polaridade < -0.1:
        return 'Negativo'
    else:
        return 'Neutro'

def aplicar_sentimento(df_feedbacks):
    df_feedbacks['Sentimento'] = df_feedbacks['Comentário'].apply(analisar_sentimento)
    return df_feedbacks

if __name__ == "__main__":
    df = pd.read_csv('feedbacks.csv')
    df_com_sentimento = aplicar_sentimento(df)
    df_com_sentimento.to_csv('feedbacks_analisados.csv', index=False)
    print("Feedbacks analisados salvos em 'feedbacks_analisados.csv'")