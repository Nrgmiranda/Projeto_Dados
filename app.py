import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote

st.set_page_config(page_title="Relatório da Felicidade Mundial", layout="wide")

st.title("📊 Relatório da Felicidade Mundial (2011–2024)")

@st.cache_data
def carregar_dados():
    sheet_id = "1YSeoTdFP_ufNasAWSXWFCzNABEAJlCM6"
    sheet_name = "Data for Figure 2.1 (2011–2024)"
    encoded_sheet_name = quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&sheet={encoded_sheet_name}"
    df = pd.read_excel(url)
    return df

df = carregar_dados()

df.columns = [
    "Ano", "Posição", "País", "Pontuação da Escada", "Limite Superior", "Limite Inferior",
    "PIB per capita (log)", "Apoio social", "Expectativa de vida saudável",
    "Liberdade para escolhas de vida", "Generosidade", "Percepção de corrupção",
    "Distopia + Resíduo"
]

# Filtros
paises = sorted(df["País"].unique())
ano_mais_recente = df["Ano"].max()
top5_paises_felizes = (
    df[df["Ano"] == ano_mais_recente]
    .sort_values(by="Pontuação da Escada", ascending=False)
    .head(5)["País"]
    .tolist()
)

paises_selecionados = st.sidebar.multiselect(
    "Escolha os países", paises, default=top5_paises_felizes
)

anos = sorted(df["Ano"].unique(), reverse=True)
ano_selecionado = st.sidebar.selectbox("Escolha o ano", anos)

df_filtrado = df[(df["País"].isin(paises_selecionados)) & (df["Ano"] == ano_selecionado)]
df_anos_selecionados = df[df["País"].isin(paises_selecionados)]

# Layout com 2 colunas para tabela e gráfico principal
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"📅 Dados de {ano_selecionado}")
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

with col2:
    st.subheader("🎯 Pontuação da Felicidade (Barra)")
    fig1 = px.bar(
        df_filtrado.sort_values("Pontuação da Escada", ascending=True),
        x="Pontuação da Escada",
        y="País",
        orientation="h",
        color="País",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={"Pontuação da Escada": "Pontuação da Felicidade"},
        title=f"Ranking da Felicidade em {ano_selecionado}"
    )
    fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("🧭 Indicadores que explicam a felicidade (Radar)")
data_radar = df_filtrado.set_index("País")[[
    "PIB per capita (log)",
    "Apoio social",
    "Expectativa de vida saudável",
    "Liberdade para escolhas de vida",
    "Generosidade",
    "Percepção de corrupção"
]]

fig2 = go.Figure()
cores = px.colors.qualitative.Plotly
for i, pais in enumerate(data_radar.index):
    fig2.add_trace(go.Scatterpolar(
        r=data_radar.loc[pais].values,
        theta=data_radar.columns,
        fill='toself',
        name=pais,
        line=dict(color=cores[i % len(cores)], width=2)
    ))

fig2.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 2])),
    showlegend=True,
    margin=dict(t=20, b=20)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("📈 Evolução da Felicidade ao Longo dos Anos (Linha)")
fig3 = px.line(
    df_anos_selecionados,
    x="Ano",
    y="Pontuação da Escada",
    color="País",
    markers=True,
    title="Tendência da Felicidade (2011-2024)",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig3.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("📊 Boxplot da Pontuação da Escada por País")
fig4 = px.box(
    df_anos_selecionados,
    x="País",
    y="Pontuação da Escada",
    color="País",
    title="Distribuição da Pontuação da Felicidade por País",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)
fig4.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("🔍 Relação: Generosidade vs Percepção de Corrupção")
fig5 = px.scatter(
    df_filtrado,
    x="Generosidade",
    y="Percepção de corrupção",
    color="País",
    size="Pontuação da Escada",
    hover_name="País",
    title=f"Generosidade vs Percepção de Corrupção em {ano_selecionado}",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig5.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("🌐 Correlação entre Indicadores (Heatmap)")

corr_cols = [
    "Pontuação da Escada",
    "PIB per capita (log)",
    "Apoio social",
    "Expectativa de vida saudável",
    "Liberdade para escolhas de vida",
    "Generosidade",
    "Percepção de corrupção"
]
corr = df_filtrado[corr_cols].corr()

fig6 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    origin='upper',
    title="Matriz de Correlação dos Indicadores",
)
fig6.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.subheader("🔎 Gráfico 3D: PIB, Apoio Social e Expectativa de Vida Saudável")

fig7 = px.scatter_3d(
    df_filtrado,
    x="PIB per capita (log)",
    y="Apoio social",
    z="Expectativa de vida saudável",
    color="País",
    size="Pontuação da Escada",
    hover_name="País",
    title=f"Relação 3D dos Indicadores em {ano_selecionado}",
    color_discrete_sequence=px.colors.qualitative.G10,
)
fig7.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig7, use_container_width=True)

st.caption("Fonte: Relatório Mundial da Felicidade - Dados públicos do Google Sheets")
