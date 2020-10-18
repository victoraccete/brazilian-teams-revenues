# This Python file uses the following encoding: utf-8
"""
Author: @victoraccete
Please note that this script was made in 2020 to get data from 2007 to 2019.
It might not be maintained to keep up to date.
The goal of this code is to generate a .csv with data from 2007 to 2019 to then
make a EDA on this data.
"""
import pandas as pd

GREAT_CLUBS = (
    'Flamengo',
    'Vasco',
    'Fluminense',
    'Botafogo',
    'Grêmio',
    'Internacional',
    'Corinthians',
    'Palmeiras',
    'São Paulo',
    'Santos',
    'Cruzeiro',
    'Atlético Mineiro'
    )

def get_tables():
    """From wikipedia"""
    URL = 'https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro'
    tables_list = pd.read_html(URL)
    return tables_list

def keep_greater_teams(tables: list) -> list:
    for index in range(0, len(tables)):
        df = tables[index]
        tables[index] = df[df.Clube.isin(GREAT_CLUBS)]
    return tables

def include_years_to_dfs(tables: list) -> list:
    def include(df, year):
        """adds a new column to the given df with a given year"""
        df['Ano'] = year
        return df

    # from 2019 to 2006 is the order found on wikipedia tables
    year_it = iter([x for x in range (2019, 2006, -1)])
    tables = [include(df, next(year_it)) for df in tables]

    return tables

############## Main block ##############
def main():
    tables = keep_greater_teams(get_tables()) # we only want the so-called 12 big
    tables = include_years_to_dfs(tables)
    df = pd.concat(tables)
    print(df)

if __name__ == "__main__":
    main()
########## end of main block ##########
