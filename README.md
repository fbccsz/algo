import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Listas base
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre']
transportadoras = ['LogExpress', 'RápidoCarga', 'TransLog', 'ViaEntrega']
status_entrega = ['Entregue', 'Em trânsito', 'Atrasada']

feedbacks_positivos = [
    "Entrega foi super rápida!", "Muito satisfeito com o serviço.", "Tudo chegou direitinho.",
    "Parabéns pela agilidade!", "Excelente experiência."
]

feedbacks_negativos = [
    "Demorou demais.", "Minha encomenda chegou danificada.", "Péssimo atendimento.",
    "A entrega atrasou muito.", "Serviço muito ruim."
]

feedbacks_neutros = [
    "Recebi hoje.", "Normal.", "Nada demais.", "Chegou.", "Tudo certo, apenas."
]

def gerar_dados_entregas(qtd=200):
    data_entregas = []

    for _ in range(qtd):
        cidade = random.choice(cidades)
        transportadora = random.choice(transportadoras)
        data = datetime.today() - timedelta(days=random.randint(0, 30))
        distancia_km = random.randint(10, 500)
        tempo_estimado = distancia_km / random.uniform(40, 60)  # horas
        tempo_real = tempo_estimado + random.uniform(-1, 3)  # atraso possível
        status = 'Entregue' if tempo_real <= tempo_estimado + 1 else 'Atrasada'
        custo = round(distancia_km * random.uniform(0.8, 2.0), 2)

        data_entregas.append({
            'Data': data.date(),
            'Cidade': cidade,
            'Transportadora': transportadora,
            'Distância_km': distancia_km,
            'Tempo_estimado_h': round(tempo_estimado, 2),
            'Tempo_real_h': round(tempo_real, 2),
            'Status': status,
            'Custo_R$': custo
        })

    return pd.DataFrame(data_entregas)

def gerar_feedbacks(qtd=100):
    comentarios = []

    for _ in range(qtd):
        tipo = random.choices(['positivo', 'negativo', 'neutro'], weights=[0.5, 0.3, 0.2])[0]
        if tipo == 'positivo':
            comentario = random.choice(feedbacks_positivos)
        elif tipo == 'negativo':
            comentario = random.choice(feedbacks_negativos)
        else:
            comentario = random.choice(feedbacks_neutros)

        comentarios.append({'Comentário': comentario})

    return pd.DataFrame(comentarios)

if __name__ == "__main__":
    entregas_df = gerar_dados_entregas()
    feedbacks_df = gerar_feedbacks()

    entregas_df.to_csv('entregas.csv', index=False)
    feedbacks_df.to_csv('feedbacks.csv', index=False)
    print("Arquivos 'entregas.csv' e 'feedbacks.csv' gerados com sucesso!")

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



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sentiment_analysis import aplicar_sentimento

st.set_page_config(page_title="LogiData - Big Data na Logística", layout="wide")

st.title("LogiData - Big Data na Logística")

# Menu lateral
menu = st.sidebar.selectbox("Escolha a seção", ["Análise de Entregas", "Feedbacks de Clientes"])

# --- Análise de Entregas ---
if menu == "Análise de Entregas":
    st.header("Visão Geral das Entregas")
    df = pd.read_csv('entregas.csv')

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Entregas", len(df))
        st.metric("Custo Total (R$)", round(df["Custo_R$"].sum(), 2))
    with col2:
        atrasadas = df[df["Status"] == "Atrasada"]
        pct_atraso = len(atrasadas) / len(df) * 100
        st.metric("Entregas Atrasadas (%)", f"{pct_atraso:.1f}%")

    st.subheader("Entregas por Cidade")
    cidade_count = df['Cidade'].value_counts()
    st.bar_chart(cidade_count)

    st.subheader("Custo Médio por Transportadora")
    custo_medio = df.groupby("Transportadora")["Custo_R$"].mean().sort_values()
    st.bar_chart(custo_medio)

    st.subheader("Status das Entregas")
    status_count = df["Status"].value_counts()
    st.dataframe(status_count.rename("Quantidade"))

# --- Feedbacks ---
elif menu == "Feedbacks de Clientes":
    st.header("Análise de Sentimentos dos Clientes")
    df_feedbacks = pd.read_csv("feedbacks.csv")
    df_com_sentimento = aplicar_sentimento(df_feedbacks)

    st.subheader("Distribuição dos Sentimentos")
    sentimento_count = df_com_sentimento["Sentimento"].value_counts()
    st.bar_chart(sentimento_count)

    st.subheader("Exemplos de Comentários")
    for sentimento in ['Positivo', 'Neutro', 'Negativo']:
        st.markdown(f"**{sentimento}s**")
        exemplos = df_com_sentimento[df_com_sentimento["Sentimento"] == sentimento].sample(2)
        for i, row in exemplos.iterrows():
            st.write(f"- {row['Comentário']}")

    st.subheader("Nuvem de Palavras dos Comentários")
    all_text = " ".join(df_com_sentimento["Comentário"].tolist())
    wc = WordCloud(width=800, height=300, background_color='white').generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)



