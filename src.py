import pandas as pd
import numpy as np
import streamlit as st

st.title('Premier League: Interactive Data Analysis')

df_epl = pd.read_csv('Data/epl_data.csv')
df_epl['Season'] = df_epl['Season'].map(lambda x: x.split('/')[0]).astype('int64')

st.write("Sample of the dataset:", df_epl.tail(20))
club = st.selectbox('Club:', df_epl['Team_Home'].unique())
period = st.slider('Period:',
                   int(df_epl['Season'].min()),
                   int(df_epl['Season'].max()),
                   (2010, 2018))

df_club = df_epl[
    ((df_epl['Team_Home'] == club) | (df_epl['Team_Away'] == club)) &
    (df_epl['Season'].between(period[0], period[1], inclusive=True))]
df_club['HomeTeam'] = df_club['Team_Home'].map(lambda x: True if (x == club) else False)

def findResult(row):
    if (row['AG'] == row['HG']):
        return 'Draw'
    elif (((row['HomeTeam'] == True) & (row['HG'] > row['AG'])) |
          ((row['HomeTeam'] == False) & (row['AG'] > row['HG']))):
        return 'Won'
    else:
        return 'Lost'

df_club['Result'] = df_club.apply(findResult, axis=1)

match_stats = {'Games played': len(df_club),
               'Won': len(df_club[df_club['Result'] == 'Won']),
               'Lost': len(df_club[df_club['Result'] == 'Lost']),
               'Draws': len(df_club[df_club['Result'] == 'Draw'])}

st.write(match_stats)
