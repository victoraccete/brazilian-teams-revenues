import pandas as pd

URL = 'https://pt.wikipedia.org/wiki/Lista_de_faturamento_dos_clubes_de_futebol_brasileiro'
tables_list = pd.read_html(URL)
