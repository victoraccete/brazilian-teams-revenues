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
    data = pd.read_csv('2007-2019.csv')
    data = data.drop(columns=['Posição', 'Deficit ou Superavit'])
    data['Faturamento'] = fix_currency_col(data['Faturamento'])
    return data
data = load_data()

@st.cache(persist=True)
def group_states(df: pd.DataFrame, group_years=True):
    """Returns two dataframes, grouped by states.
    The first is grouped by the sum, and the second by the mean."""
    if group_years == True:
        df_sum = df.groupby(['Estado']).sum().drop(columns=['Ano']).reset_index()
        df_mean = df.groupby(['Estado']).mean().drop(columns=['Ano']).reset_index()
    else:
        df_sum = df.groupby(['Estado', 'Ano']).sum().reset_index()
        df_mean = df.groupby(['Estado', 'Ano']).mean().reset_index()
    return df_sum, df_mean

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
        # We use this > 0 to see if the user really selected something.
        # If the user didn't. Then we'll do nothing to the dataset and keep it full.
        modified_data = subset_by_column(data, state_choice, 'Estado')
    else:
        pass

    # -------- YEAR SELECTION -------- #
    years = [yr for yr in range(2007, 2020)]
    year_choice = st.sidebar.multiselect('Escolher anos:', years)
    if len(year_choice) > 0:
        # We use this > 0 to see if the user really selected something.
        # If the user didn't. Then we'll do nothing to the dataset and keep it full.
        modified_data = subset_by_column(data, year_choice, 'Ano')
    else:
        pass

    st.write(modified_data)
    pass

if st.sidebar.checkbox("Comparativo entre clubes", True):
    st.markdown("## Comparativo entre clubes:")
    clubs_line_plot = px.line(data,
                        x="Ano",
                        y="Faturamento",
                        color='Clube',
                        title='Receitas dos 12 grandes',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
    clubs_line_plot.update_xaxes(showgrid=False)
    clubs_line_plot.update_yaxes(showgrid=False)
    st.plotly_chart(clubs_line_plot)

    club_sum_data = data.groupby(['Clube', 'Estado']).sum().drop(columns=['Ano']).reset_index()
    clubs_bar_plot = px.bar(club_sum_data,
                    x='Clube',
                    y='Faturamento',
                    color='Clube',
                    title='Faturamento total no período 2007-2019',
                    labels={
                        'Faturamento': 'Faturamento (Milhões)'
                        },
                    template='plotly_white',
                    )
    clubs_bar_plot.update_xaxes(showgrid=False)
    clubs_bar_plot.update_yaxes(showgrid=False)
    st.plotly_chart(clubs_bar_plot)
    pass

if st.sidebar.checkbox("Comparativo entre estados", False):
    st.markdown("## Comparativo entre estados")
    df_sum, df_mean = group_states(data)
    df_sum_years, df_mean_years = group_states(data, group_years=False)
    options = ('Média dos clubes', 'Soma')
    bar_choice = st.radio("Forma de agrupamento", options)
    if bar_choice == 'Média dos clubes':
        states_line_plot = px.line(df_mean_years,
                            x="Ano",
                            y="Faturamento",
                            color='Estado',
                            title='Média incluindo os grandes clubes',
                            labels={
                                'Faturamento': 'Faturamento (Milhões)'
                                },
                            template='plotly_white',
                            )
        states_line_plot.update_xaxes(showgrid=False)
        states_line_plot.update_yaxes(showgrid=False)
        st.plotly_chart(states_line_plot)

        states_bar_plot = px.bar(df_mean,
                        x='Estado',
                        y='Faturamento',
                        title='Média de faturamento incluindo os grandes clubes (2007-2019)',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
        states_bar_plot.update_xaxes(showgrid=False)
        states_bar_plot.update_yaxes(showgrid=False)
        st.plotly_chart(states_bar_plot)
    else:
        states_line_plot = px.line(df_sum_years,
                            x="Ano",
                            y="Faturamento",
                            color='Estado',
                            title='Soma incluindo os grandes clubes',
                            labels={
                                'Faturamento': 'Faturamento (Milhões)'
                                },
                            template='plotly_white',
                            )
        states_line_plot.update_xaxes(showgrid=False)
        states_line_plot.update_yaxes(showgrid=False)
        st.plotly_chart(states_line_plot)

        states_bar_plot = px.bar(df_sum,
                        x='Estado',
                        y='Faturamento',
                        title='Soma de faturamento incluindo os grandes clubes (2007-2019)',
                        labels={
                            'Faturamento': 'Faturamento (Milhões)'
                            },
                        template='plotly_white',
                        )
        states_bar_plot.update_xaxes(showgrid=False)
        states_bar_plot.update_yaxes(showgrid=False)
        st.plotly_chart(states_bar_plot)

    pass
