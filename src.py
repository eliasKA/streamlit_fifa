import pandas as pd
import streamlit as st
import numpy as np

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
    (df_epl['Season'].between(period[0], period[1], inclusive=True))
    ]

match_stats = {'Games played': len(df_club),
               'Won (Home)': len(df_club[(df_club['Team_Home'] == club) & (df_club['HG'] > df_club['AG'])]),
               'Lost (Home)': len(df_club[(df_club['Team_Home'] == club) & (df_club['HG'] < df_club['AG'])]),
               'Won (Away)': len(df_club[(df_club['Team_Away'] == club) & (df_club['AG'] > df_club['HG'])]),
               'Lost (Away)': len(df_club[(df_club['Team_Away'] == club) & (df_club['AG'] < df_club['HG'])]),
               'Draws': len(df_club[df_club['AG'] == df_club['HG']]),
               'Clean sheets': len(df_club[((df_club['Team_Away'] == club) & (df_club['HG'] == 0)) &
                                           ((df_club['Team_Home'] == club) & (df_club['AG'] == 0))]),
               'Jantjes': len(df_club[((df_club['Team_Away'] == club) & ((df_club['AG'] - df_club['HG']) >= 3)) &
                                      ((df_club['Team_Home'] == club) & ((df_club['HG'] - df_club['AG']) >= 3))])}

match_stats['Won (Total)'] = match_stats['Won (Home)'] + match_stats['Won (Away)']
match_stats['Lost (Total)'] = match_stats['Lost (Home)'] + match_stats['Lost (Away)']

st.write(match_stats)
