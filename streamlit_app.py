# Imports
import streamlit as st
import pandas as pd
import altair as alt

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
    year_dropdown = alt.binding_select(options=olympics['Year'].unique().tolist())
    year_selector = alt.selection_single(fields=['Year'], bind=year_dropdown, name='Select Year')

    country_dropdown = alt.binding_select(options=olympics['Country'].unique().tolist())
    country_selector = alt.selection_single(fields=['Country'], bind=country_dropdown, name='Select Country')

    season_radio = alt.binding_radio(options=olympics['Season'].unique().tolist())
    season_selector = alt.selection_single(fields=['Season'], bind=season_radio, name='Select Season')

x = st.slider("Select a value")
st.write(x, "squared is", x * x)
