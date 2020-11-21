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

def subset_by_column(df: pd.DataFrame, values: list, col: str) -> pd.DataFrame:
    """Receives as input a dataframe, a list of values to subset and the name
    the column as a string. Then, for the given column, subset the df with the
    values from within the list.
    Returns the updated dataframe."""
    df = df.loc[df[col].isin(values)]
    return df

if st.sidebar.checkbox("Tabela", False): # this 'False' param defines the default value
    st.markdown("## Tabela:")

    modified_data = data.copy()
    # -------- STATE SELECTION -------- #
    states = ('Rio de Janeiro', 'São Paulo', 'Minas Gerais', 'Rio Grande do Sul')
    state_choice = st.sidebar.multiselect('Escolher estados:', states)
    if len(state_choice) > 0:
        modified_data = subset_by_column(data, state_choice, 'Estado')

    # -------- YEAR SELECTION -------- #
    years = [yr for yr in range(2007, 2020)]
    year_choice = st.sidebar.multiselect('Escolher anos:', years)
    if len(year_choice) > 0:
        modified_data = subset_by_column(data, year_choice, 'Ano')

    st.write(modified_data)
    pass

if st.sidebar.checkbox("Gráfico de linha", True):
    color_list = [
            '#D62728', # Flamengo
            '#52A24B', # Palmeiras
            '#17BECF', # Grêmio
            '#FB0D0D', # Internacional
            '#101010', # Corinthians
            '#BAB0AC', # Santos
            '#E45756', # São Paulo
            '#808080', # Atlético MG
            '#1F77B4', # Cruzeiro
            '#66AA00', # Fluminense
            '#9D755D', # Vasco
            '#303030', # Botafogo
        ]
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
                        color_discrete_sequence=color_list,
                        )
    fig_revs.update_xaxes(showgrid=False)
    fig_revs.update_yaxes(showgrid=False)
    st.plotly_chart(fig_revs)
    pass

@st.cache(persist=True)
def group_states(df: pd.DataFrame):
    """Returns two dataframes, grouped by states.
    The first is grouped by the sum, and the second by the mean."""
    df_sum = df.groupby(['Estado']).sum().drop(columns=['Ano']).reset_index()
    df_mean = df.groupby(['Estado']).mean().drop(columns=['Ano']).reset_index()
    return df_sum, df_mean

if st.sidebar.checkbox("Comparativo total por estado", False):
    st.markdown("## Comparativo de todos os anos: ")
    color_list = [
            '#D62728', # Flamengo
            '#52A24B', # Palmeiras
            '#17BECF', # Grêmio
            '#FB0D0D', # Internacional
            '#101010', # Corinthians
            '#BAB0AC', # Santos
            '#E45756', # São Paulo
            '#808080', # Atlético MG
            '#1F77B4', # Cruzeiro
            '#66AA00', # Fluminense
            '#9D755D', # Vasco
            '#303030', # Botafogo
        ]
    options = ('Média', 'Soma')
    bar_choice = st.radio("Forma de agrupamento", options)
    df_sum, df_mean = group_states(data)
    if bar_choice == 'Média':
        fig_bar = px.bar(df_mean,
                        x='Estado',
                        y='Faturamento',
                        title='Média de faturamento dos clubes de cada estado (2007-2019)',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(showgrid=False)
        st.plotly_chart(fig_bar)
    else:
        fig_bar = px.bar(df_sum,
                        x='Estado',
                        y='Faturamento',
                        title='Soma de faturamento dos clubes de cada estado (2007-2019)',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(showgrid=False)
        st.plotly_chart(fig_bar)
    pass
