import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel de Emprego", layout="wide")

st.title("Painel de Emprego: Ministério, SEBRAE e Indústria")
st.write("Fonte dos dados: Agência de Notícias do IBGE (PNAD Contínua)")

# Tabela
dados_projeto = [
    # Dados de 2012
    {'UF': 'SP', 'Regiao': 'Sudeste', 'Ano': 2012, 'Desemprego': 6.9, 'Informalidade': 35.0, 'Trabalhadores': 32.8, 'Tipo': 'Com Carteira'},
    {'UF': 'RJ', 'Regiao': 'Sudeste', 'Ano': 2012, 'Desemprego': 7.5, 'Informalidade': 36.5, 'Trabalhadores': 10.5, 'Tipo': 'Sem Carteira'},
    {'UF': 'MG', 'Regiao': 'Sudeste', 'Ano': 2012, 'Desemprego': 6.2, 'Informalidade': 38.0, 'Trabalhadores': 20.1, 'Tipo': 'Conta Própria'},
    {'UF': 'BA', 'Regiao': 'Nordeste', 'Ano': 2012, 'Desemprego': 9.2, 'Informalidade': 48.0, 'Trabalhadores': 5.1, 'Tipo': 'Doméstico'},
    {'UF': 'PR', 'Regiao': 'Sul', 'Ano': 2012, 'Desemprego': 5.1, 'Informalidade': 31.0, 'Trabalhadores': 21.1, 'Tipo': 'Outros'},
    {'UF': 'AM', 'Regiao': 'Norte', 'Ano': 2012, 'Desemprego': 8.0, 'Informalidade': 45.0, 'Trabalhadores': 0.0, 'Tipo': 'Nenhum'},
    {'UF': 'MT', 'Regiao': 'Centro-Oeste', 'Ano': 2012, 'Desemprego': 5.8, 'Informalidade': 34.0, 'Trabalhadores': 0.0, 'Tipo': 'Nenhum'},

    # Dados de 2022
    {'UF': 'SP', 'Regiao': 'Sudeste', 'Ano': 2022, 'Desemprego': 9.0, 'Informalidade': 38.2, 'Trabalhadores': 35.9, 'Tipo': 'Com Carteira'},
    {'UF': 'RJ', 'Regiao': 'Sudeste', 'Ano': 2022, 'Desemprego': 10.1, 'Informalidade': 39.0, 'Trabalhadores': 12.9, 'Tipo': 'Sem Carteira'},
    {'UF': 'MG', 'Regiao': 'Sudeste', 'Ano': 2022, 'Desemprego': 8.2, 'Informalidade': 40.1, 'Trabalhadores': 25.5, 'Tipo': 'Conta Própria'},
    {'UF': 'BA', 'Regiao': 'Nordeste', 'Ano': 2022, 'Desemprego': 12.5, 'Informalidade': 51.3, 'Trabalhadores': 5.8, 'Tipo': 'Doméstico'},
    {'UF': 'PR', 'Regiao': 'Sul', 'Ano': 2022, 'Desemprego': 6.5, 'Informalidade': 33.4, 'Trabalhadores': 17.9, 'Tipo': 'Outros'},
    {'UF': 'AM', 'Regiao': 'Norte', 'Ano': 2022, 'Desemprego': 10.5, 'Informalidade': 49.2, 'Trabalhadores': 0.0, 'Tipo': 'Nenhum'},
    {'UF': 'MT', 'Regiao': 'Centro-Oeste', 'Ano': 2022, 'Desemprego': 7.2, 'Informalidade': 36.8, 'Trabalhadores': 0.0, 'Tipo': 'Nenhum'}
]

df = pd.DataFrame(dados_projeto)


st.sidebar.write("Filtros")
ano_escolhido = st.sidebar.selectbox("Escolha o Ano:", options=[2012, 2022])
regiao_escolhida = st.sidebar.multiselect("Escolha as Regiões:", options=['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'], default=['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'])

dados_filtrados = df[(df['Ano'] == ano_escolhido) & (df['Regiao'].isin(regiao_escolhida))]

st.subheader(f"Resultados para o ano de {ano_escolhido}")

# Médias e medianas simples
if not dados_filtrados.empty:
    media_desemprego = dados_filtrados['Desemprego'].mean()
    mediana_desemprego = dados_filtrados['Desemprego'].median()
else:
    media_desemprego = 0
    mediana_desemprego = 0

st.write(f"Média de Desemprego: {media_desemprego:.1f}%")
st.write(f"Mediana de Desemprego: {mediana_desemprego:.1f}%")


st.write("Gráficos de Análise")

# Gráfico de Pizza
dados_para_pizza = dados_filtrados[dados_filtrados['Trabalhadores'] > 0]
fig_pizza = px.pie(dados_para_pizza, values='Trabalhadores', names='Tipo', title=f"Distribuição da População Ocupada em {ano_escolhido} (em Milhões de Pessoas)")
st.plotly_chart(fig_pizza)

# Gráfico de barras
fig_barra = px.bar(dados_filtrados, x='UF', y='Desemprego', color='Regiao', title="Ranking de Desemprego por Estado (Visão Indústria/SEBRAE)")
st.plotly_chart(fig_barra)

# Gráfico de boxplot
fig_box = px.box(dados_filtrados, x='Regiao', y='Desemprego', title="Distribuição do Desemprego por Região (Visão Ministério)")
st.plotly_chart(fig_box)


st.write("Conclusão para a Banca")

if media_desemprego > mediana_desemprego:
    st.write("Para a Ministra: A média deu maior que a mediana. Isso significa que existem alguns estados com o desemprego muito alto, puxando a média para cima. O Ministério deve focar neles.")
else:
    st.write("Para a Ministra: O desemprego está distribuído de forma equilibrada entre as regiões selecionadas.")

st.write("Foco SEBRAE: Como o gráfico de pizza mostra que muita gente trabalha por conta própria ou sem carteira assinada, exige incentivos para que microempresas saiam da ilegalidade.")
st.write("Foco Indústria: Estados com muito desemprego no ranking têm mais mão de obra disponível para novas fábricas.")
