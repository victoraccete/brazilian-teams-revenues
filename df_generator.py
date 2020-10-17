'''
Author: @victoraccete
Please note that this script was made in 2020 to get data from 2007 to 2019.
It might not be maintained to keep up to date.
The goal of this code is to generate a .csv with data from 2007 to 2019 to then
make a EDA on this data.'''
import pandas as pd

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



############## Main block ##############
def main():
    print(df_dict(get_tables()).keys())

if __name__ == "__main__":
    main()
########## end of main block ##########
