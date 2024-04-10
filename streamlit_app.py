# Imports
import streamlit as st
import pandas as pd
import panel as pn
import altair as alt

# Panel Extension
pn.extension()
pn.extension('vega')

# Page configuration
st.set_page_config(
    page_title="Olympic Games Medals",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded")

# Data Files Loading
summer_olympics = pd.read_csv('SummerOlympics.csv')
winter_olympics = pd.read_csv('WinterOlympics.csv')

# Creation of the 'Season' Column
summer_olympics['Season']='summer'
winter_olympics['Season']='winter'

# Concatenation of the two tables to have a unique table
olympics = pd.concat([summer_olympics, winter_olympics], ignore_index=True).sort_values(by='Year')

# Creation of the columns 'Gold', 'Silver' and 'Bronze'
olympics['Gold']=olympics['Medal'].apply(lambda x: 1 if x == 'Gold' else 0)
olympics['Silver']=olympics['Medal'].apply(lambda x: 1 if x == 'Silver' else 0)
olympics['Bronze']=olympics['Medal'].apply(lambda x: 1 if x == 'Bronze' else 0)

# Sidebar
with st.sidebar:
    st.title('🥇 Olympic Games Medals')

    # Define dropdown selectors for season, year, and country
    season_dropdown = pn.widgets.Select(options=['summer', 'winter'], name='Select Season')
    year_dropdown = pn.widgets.Select(name='Select Year')
    country_dropdown = pn.widgets.Select(name='Select Country')

x = st.slider("Select a value")
st.write(x, "squared is", x * x)
