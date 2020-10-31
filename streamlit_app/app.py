import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.title("Análise de faturamento dos clubes brasileiros")
st.markdown("Apenas dados dos considerados '12 grandes'. \
Dados extraídos da [Wikipedia](https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro) \
de 2007 a 2019.")
st.markdown("Use a barra lateral para escolher opções de visualização.")
st.sidebar.title("Opções de visualização")

@st.cache(persist=True)
def load_data() -> pd.DataFrame:
    data = pd.read_csv('')
    return data
