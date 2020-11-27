# brazilian-teams-revenues
Analysing the revenues from all of the so-called 12 Great football/soccer clubs in Brazil. 

#### You can check it out online without any setupt on [Streamlit share](https://share.streamlit.io/victoraccete/brazilian-teams-revenues/main)!

[Notebook](https://github.com/victoraccete/brazilian-teams-revenues/blob/main/Brazilian_teams_analysis.ipynb) made with Colab. There's a link to it in the .ipynb file. The notebook is in English.  

The [csv_generator.py](https://github.com/victoraccete/brazilian-teams-revenues/blob/main/csv_generator.py) file downloads the tables from Wikipedia page and perform some initial data manipulation to generate [this dataset](https://github.com/victoraccete/brazilian-teams-revenues/blob/main/dataset/2007-2019.csv). This dataset is used in the Notebook and the streamlit app.  

The [streamlit app](https://github.com/victoraccete/brazilian-teams-revenues/blob/main/streamlit_app.py) and the dataset are the only files needed to run the streamlit app, if you have the requirements installed. The requirements are in [requirements.txt](https://github.com/victoraccete/brazilian-teams-revenues/blob/main/requirements.txt).  

Run with: ```streamlit run streamlit_app.py```
