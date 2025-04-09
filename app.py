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
    
    comentarios_filtrados = df_com_sentimento[df_com_sentimento["Sentimento"] == sentimento]

    if comentarios_filtrados.empty:
        st.write("- Nenhum comentário disponível.")
    else:
        exemplos = comentarios_filtrados.sample(n=min(2, len(comentarios_filtrados)), random_state=42)
        for i, row in exemplos.iterrows():
            st.write(f"- {row['Comentário']}")


    st.subheader("Nuvem de Palavras dos Comentários")
    all_text = " ".join(df_com_sentimento["Comentário"].tolist())
    wc = WordCloud(width=800, height=300, background_color='white').generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
