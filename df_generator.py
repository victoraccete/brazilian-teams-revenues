'''
Author: @victoraccete
Please note that this script was made in 2020 to get data from 2007 to 2019.
It might not be maintained to keep up to date.
The goal of this code is to generate a .csv with data from 2007 to 2019 to then
make a EDA on this data.'''
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
    URL = 'https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro'
    tables_list = pd.read_html(URL)
    return tables_list

def df_dict(tables: list) -> dict:
    '''
    Returns a dictionary where the key is the year and the value is
    the corresponding dataframe.
    '''
    df_dict = {}
    tab_it = iter(tables)
    for year in range(2019, 2006, -1):
        df_dict[year] = next(tab_it)
    return df_dict

def keep_greater_teams(tables: list) -> list:
    for index in range(0, len(tables)):
        df = tables[index]
        tables[index] = df[df.Clube.isin(GREAT_CLUBS)]
    return tables

def include_years_to_df_list(tables: list) -> list:
     def include_year(df, year):
         '''adds a new column to the given df with a given year'''
         df['Year'] = year
         return df
     # iterator used to help including years from 2019 to 2006 in descending order
     year_it = iter([x for x in range (2019, 2006, -1)])
     tables = [include_year(df, next(year_it)) for df in tables]

     return tables

############## Main block ##############
def main():
    tables = keep_greater_teams(get_tables())
    tables = include_years_to_df_list(tables)
    print(tables[0])

if __name__ == "__main__":
    main()
########## end of main block ##########
