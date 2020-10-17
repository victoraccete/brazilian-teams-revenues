'''
Author: @victoraccete
Please note that this script was made in 2020 to get data from 2007 to 2019.
It might not be maintained to keep up to date.
The goal of this code is to generate a .csv with data from 2007 to 2019 to then
make a EDA on this data.
'''
import pandas as pd

def get_tables():
    URL = 'https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro'
    tables_list = pd.read_html(URL)
    return tables_list
