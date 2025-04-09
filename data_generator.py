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