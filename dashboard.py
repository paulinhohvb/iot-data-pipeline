import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conexão com o banco de dados
engine = create_engine('postgresql://postgres:senha123@localhost:5432/postgres')

# Função para carregar dados de uma view
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name.strip()}", engine)

# Função para aplicar filtros de data
def filter_by_date(df, start_date, end_date):
    df['noted_date'] = pd.to_datetime(df['noted_date'], format='%d-%m-%Y %H:%M', errors='coerce')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return df[(df['noted_date'] >= start_date) & (df['noted_date'] <= end_date)]

# Título do dashboard
st.title('Dashboard de Temperaturas IoT')


# Exibição do gráfico 1 - Média de temperatura por dispositivo
st.header('Média de Temperatura por Dispositivo')
df_avg_temp = load_data('temperature_readings')

# Convertendo 'temp' para float e corrigindo a escala da temperatura
df_avg_temp['temp'] = df_avg_temp['temp'].astype(float) / 100000  # Ajuste para a escala correta

# Criação do gráfico
fig1 = px.bar(
    df_avg_temp,
    x='room_id/id', 
    y='temp',
    title='Média de Temperatura por Dispositivo',
    labels={'room_id/id': 'ID do Dispositivo', 'temp': 'Temperatura (°C)'},
)

# Corrigir a escala do eixo Y para mostrar valores corretamente
fig1.update_layout(
    yaxis=dict(
        tickformat=".1f",  # Forçar uma casa decimal para mostrar a temperatura corretamente
        title="Temperatura (°C)"
    ),
    xaxis_title="ID do Dispositivo",
    plot_bgcolor='white'
)

st.plotly_chart(fig1)


# Gráfico 2: Contagem de leituras por hora
st.header('Leituras por Hora do Dia')
df_leituras_hora = load_data('contagem_leituras_por_hora')
fig2 = px.line(
    df_leituras_hora,
    x='hora',
    y='total_leituras',
    markers=True,
    title='Contagem de Leituras por Hora'
)
fig2.update_layout(
    xaxis_title='Hora do Dia',
    yaxis_title='Total de Leituras',
    plot_bgcolor='white'
)
st.plotly_chart(fig2)

# Gráfico 3: Temperaturas máximas e mínimas por dia
st.header('Temperaturas Máximas e Mínimas por Dia')
df_temp_max_min = load_data('temp_max_min_por_dia')
df_temp_max_min['data'] = pd.to_datetime(df_temp_max_min['data'], errors='coerce')

fig3 = px.line(
    df_temp_max_min,
    x='data',
    y=['temp_max', 'temp_min'],
    labels={'value': 'Temperatura (°C)', 'data': 'Data'},
    title='Temperaturas Máximas e Mínimas por Dia'
)
fig3.update_layout(
    xaxis_title='Data',
    yaxis_title='Temperatura (°C)',
    plot_bgcolor='white'
)
st.plotly_chart(fig3)
