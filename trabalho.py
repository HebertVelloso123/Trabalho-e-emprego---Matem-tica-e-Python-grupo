import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Trabalho", layout="wide")

ufs = [
    ('RO', 'Norte'), ('AC', 'Norte'), ('AM', 'Norte'), ('RR', 'Norte'), 
    ('PA', 'Norte'), ('AP', 'Norte'), ('TO', 'Norte'), ('MA', 'Nordeste'), 
    ('PI', 'Nordeste'), ('CE', 'Nordeste'), ('RN', 'Nordeste'), ('PB', 'Nordeste'), 
    ('PE', 'Nordeste'), ('AL', 'Nordeste'), ('SE', 'Nordeste'), ('BA', 'Nordeste'), 
    ('MG', 'Sudeste'), ('ES', 'Sudeste'), ('RJ', 'Sudeste'), ('SP', 'Sudeste'), 
    ('PR', 'Sul'), ('SC', 'Sul'), ('RS', 'Sul'), ('MS', 'Centro-Oeste'), 
    ('MT', 'Centro-Oeste'), ('GO', 'Centro-Oeste'), ('DF', 'Centro-Oeste')
]

#Criação simulados
np.random.seed(42)
dados = []
for est, rgn in ufs:
    # Dados de 2012
    t1 = np.random.normal(loc=7.5 if rgn in ['Sul', 'Centro-Oeste'] else 11.0, scale=1.5)
    t2 = np.random.normal(loc=35.0 if rgn in ['Sul', 'Sudeste'] else 52.0, scale=4.0)
    dados.append({'UF': est, 'R': rgn, 'Ano': 2012, 'Des': round(max(4.0, t1), 1), 'Inf': round(t2, 1)})
    # Dados de 2022 (com aumento no desemprego e informalidade)
    dados.append({'UF': est, 'R': rgn, 'Ano': 2022, 'Des': round(max(5.0, t1 + 2.0), 1), 'Inf': round(t2 + 1.5, 1)})


df_ = pd.DataFrame(dados)


st.title("Painel de Emprego: Ministério, SEBRAE e Indústria")

ano = st.sidebar.selectbox("Escolha o Ano", options=df_['Ano'].unique())
reg = st.sidebar.multiselect("Escolha as Regiões", options=df_['R'].unique(), default=df_['R'].unique())

sub = df_[(df_['Ano'] == ano) & (df_['R'].isin(reg))]

st.subheader(f"Resultados para o ano de {ano}")

#Médias e medianas
if not sub.empty:
    med = sub['Des'].mean()
    mda = sub['Des'].median()
else:
    med, mda = 0.0, 0.0


col1, col2 = st.columns(2)
with col1:
    st.metric(label="Média de Desemprego", value=f"{med:.1f}%")
with col2:
    st.metric(label="Mediana de Desemprego", value=f"{mda:.1f}%")

st.write("---")

# gerar gráficos
st.write("Gráficos de Análise")
fig1 = px.box(sub, x='R', y='Des', title="Distribuição do Desemprego por Região (Visão Ministério)", color='R')
st.plotly_chart(fig1)

sub_ord = sub.sort_values(by='Des', ascending=False)
fig2 = px.bar(sub_ord, x='UF', y='Des', color='R', title="Ranking de Desemprego por Estado (Visão Indústria/SEBRAE)")
st.plotly_chart(fig2)

st.write("---")

# conclusão extra
st.write("Conclusão do Grupo para a Banca")
if med > mda:
    st.write("Para a Ministra: A média deu maior que a mediana. Isso significa que existem alguns estados com o desemprego muito alto, puxando a média para cima. O Ministério deve focar neles.")
elif med < mda:
    st.write("Para a Ministra: A média deu menor que a mediana. Isso significa que a maioria dos estados está com desemprego alto, mas poucos estados muito baixos puxaram a média para baixo.")
else:
    st.write("Para a Ministra: A média e a mediana são quase iguais, o desemprego está bem distribuído pelo país.")

st.markdown(f"""
Foco SEBRAE: A informalidade alta exige incentivos para que microempresas saiam da ilegalidade.
Foco Indústria: Estados com muito desemprego têm mais mão de obra disponível para novas fábricas.
""")
