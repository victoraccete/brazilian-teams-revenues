import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import re

st.title("Faturamento dos clubes brasileiros")
st.markdown("Apenas dados dos considerados '12 grandes'. \
Dados de 2007 a 2019 extraídos da \
[Wikipedia](https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro).")
st.markdown("Use a barra lateral para escolher opções de visualização.")
st.sidebar.title("Opções de visualização")

### Initial data cleaning:  ###
def clean_currency(t: str) -> str:
    """Function to clean the revenue columns, to keep only the numbers in millions."""
    t = re.sub("\[.*\]", "", t) # removes any value between [ and ].
    t = re.sub('.?[a-zA-Z].?', "", t) # removing letters from end and beginning
    t = t.strip().replace(',', '.') # removes whitespace and replaces comma
    return t

def fix_currency_col(series):
    """Gets a messy column and make it a float column"""
    # using lambda to pass the value from the series as argumento to clean_currency
    series = series.apply(lambda x: clean_currency(x))
    return series.astype('float')

@st.cache(persist=True)
def load_data() -> pd.DataFrame:
    data = pd.read_csv('../dataset/2007-2019.csv')
    #data['Ano'] = pd.to_datetime(data['Ano'], format="%Y")
    data = data.drop(columns=['Posição', 'Deficit ou Superavit'])
    data['Faturamento'] = fix_currency_col(data['Faturamento'])
    return data
data = load_data()

def subset_by_state(df: pd.DataFrame, states: list) -> pd.DataFrame:
    df = df.loc[df['Estado'].isin(states)]
    return df

if st.sidebar.checkbox("Tabela", False): # this 'False' param defines the default value
    st.markdown("## Tabela:")
    states = ('Rio de Janeiro', 'São Paulo', 'Minas Gerais', 'Rio Grande do Sul')
    state_choice = st.sidebar.multiselect('Filtrar por estados:', states)
    if len(state_choice) > 0:
        tmp_data = subset_by_state(data, state_choice)
        st.write(tmp_data)
    else:
        st.write(data)
    pass

if st.sidebar.checkbox("Gráfico de linha", True):
    st.markdown("## Gráfico:")
    fig_revs = px.line(data,
                        x="Ano",
                        y="Faturamento",
                        color='Clube',
                        title='Receitas dos 12 grandes',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
    fig_revs.update_xaxes(showgrid=False)
    fig_revs.update_yaxes(showgrid=False)
    st.plotly_chart(fig_revs)
