import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Interativo - Happiness", layout="wide")

st.title("🌍 Dashboard de Felicidade Mundial (2011–2024)")
st.markdown("Este dashboard interativo apresenta dados do Relatório Mundial da Felicidade entre 2011 e 2024.")

# Leitura do arquivo local (se estiver rodando via GitHub, substitua pelo raw link)
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/Data%20for%20Figure%202.csv"  # substitua pelo seu raw URL
    df = pd.read_csv(url)
    return df

df = carregar_dados()

# Exibição inicial do DataFrame
with st.expander("🔍 Ver dados brutos"):
    st.dataframe(df)

# Filtros
anos = sorted(df["year"].unique())
paises = sorted(df["Country name"].unique())

col1, col2 = st.columns(2)
ano_selecionado = col1.selectbox("Selecione o ano:", anos, index=len(anos)-1)
pais_selecionado = col2.multiselect("Filtrar por país:", paises, default=["Brazil", "Finland", "United States"])

df_filtrado = df[(df["year"] == ano_selecionado) & (df["Country name"].isin(pais_selecionado))]

# Gráfico de barras - Pontuação por país
fig_bar = px.bar(
    df_filtrado,
    x="Country name",
    y="Life Ladder",
    color="Country name",
    title=f"🔢 Nível de Felicidade em {ano_selecionado}",
    labels={"Life Ladder": "Nível de Felicidade"},
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de linha - Evolução histórica
df_linha = df[df["Country name"].isin(pais_selecionado)]

fig_line = px.line(
    df_linha,
    x="year",
    y="Life Ladder",
    color="Country name",
    title="📈 Evolução Histórica da Felicidade (Life Ladder)",
    markers=True,
    labels={"year": "Ano", "Life Ladder": "Nível de Felicidade"},
)
st.plotly_chart(fig_line, use_container_width=True)

# Estatísticas rápidas
with st.expander("📊 Estatísticas Descritivas"):
    st.write(df_filtrado.describe())

st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit. Dados: World Happiness Report")
