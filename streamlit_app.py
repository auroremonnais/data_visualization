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
    st.write("**Select Season**\n")
    season_button = st.radio('', ['summer', 'winter'])
    st.write("**Select Year**")
    years = olympics[olympics['Season'] == season_button]['Year'].unique()
    year_dropdown = st.selectbox('', sorted(years))
    st.write("**Select Country**")
    countries = sorted(olympics[olympics['Season'] == season_button]['Country'].unique())
    country_dropdown = st.selectbox('', countries)    

# Define a function to filter data based on selected filters
def filter_data(year, country, season):
    filtered_data = olympics[(olympics['Year'] == year) & (olympics['Country'] == country) & (olympics['Season'] == season)]
    return filtered_data

def get_country_data(country):
    filtered_data = olympics[olympics['Country'] == country]
    return filtered_data

# Define the function to create the visualization based on filtered data
def create_medal_chart(filtered_data):
    # Aggregate the filtered data to calculate total medals per type in each Olympic year
    aggregated_data = filtered_data.groupby(['Year', 'Country', 'Season']).agg(
        Gold=('Gold', 'sum'),
        Silver=('Silver', 'sum'),
        Bronze=('Bronze', 'sum')
    ).reset_index()

    # Melt the DataFrame to convert the wide format to long format
    melted_data = pd.melt(aggregated_data, id_vars=['Year', 'Country', 'Season'], var_name='Medal', value_name='Count')

    # Define color scale for medals
    medal_colors = {'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}

    # Create a bar chart
    chart = alt.Chart(melted_data).mark_bar().encode(
        x='Medal:N',  # Medal types as x-axis
        y='Count:Q',  # Count of medals as y-axis
        color=alt.Color('Medal:N', scale=alt.Scale(domain=['Gold', 'Silver', 'Bronze'], range=[medal_colors['Gold'], medal_colors['Silver'], medal_colors['Bronze']])),
    ).properties(
        width=400,
        height=400
        )
    return chart

def create_sport_chart(filtered_data):
    # Aggregate the filtered data to count the number of sports per country in each Olympic year
    aggregated_data = filtered_data.groupby(['Year', 'Country', 'Season', 'Sport']).size().reset_index(name='Count')

    # Create a pie chart
    chart = alt.Chart(aggregated_data).mark_arc().encode(
        theta='Count:Q',
        color='Sport:N',
        tooltip=['Country', 'Year', 'Season', 'Sport', 'Count']
    ).properties(
        width=400,
        height=400
    )
    return chart

def create_gender_chart(filtered_data):
    
    # Filter data for Summer and Winter Olympics
    summer_data = filtered_data[filtered_data['Season'] == 'summer']
    winter_data = filtered_data[filtered_data['Season'] == 'winter']

    # Aggregate the data to calculate total male and female athletes per country in each Olympic year for Summer Olympics
    aggregated_summer_data = summer_data.groupby(['Year', 'Country', 'Gender']).size().reset_index(name='Count')

    # Aggregate the data to calculate total male and female athletes per country in each Olympic year for Winter Olympics
    aggregated_winter_data = winter_data.groupby(['Year', 'Country', 'Gender']).size().reset_index(name='Count')

    # Create a base chart for Summer Olympics
    summer_chart = alt.Chart(aggregated_summer_data).mark_line().encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year')),
        y='Count:Q',
        color='Gender:N',
        tooltip=['Year:O', 'Gender:N', 'Count:Q']
    ).properties(
        width=400,
        height=400,
        title='Summer Olympics'
    )

    # Create a base chart for Winter Olympics
    winter_chart = alt.Chart(aggregated_winter_data).mark_line().encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year')),
        y='Count:Q',
        color='Gender:N',
        tooltip=['Year:O', 'Gender:N', 'Count:Q']
    ).properties(
        width=400,
        height=400,
        title='Winter Olympics'
    )

    # Combine the two charts
    combined_chart = alt.hconcat(summer_chart, winter_chart)

    return combined_chart

# Define the function to update the visualization when filters change
def update():
    filtered_data = filter_data(year_dropdown, country_dropdown, season_button)
    country_data = get_country_data(country_dropdown)
    medal_chart = create_medal_chart(filtered_data)
    sport_chart = create_sport_chart(filtered_data)
    gender_chart = create_gender_chart(country_data)
    return medal_chart, sport_chart, gender_chart

# Initial update
medal_chart, sport_chart, gender_chart = update()

st.title('🥇 Olympic Games Medals Data Visualization')

# Display the two first charts in two columns
col1, col2 = st.columns(2)
with col1:
    st.subheader('Distribution of Medals per Type')
    st.altair_chart(medal_chart, use_container_width=True)
with col2:
    st.subheader('Distribution of Medals per Sport')
    st.altair_chart(sport_chart, use_container_width=True)

# Display the third chart underneath the existing charts
st.subheader('Total Number of Medals by Gender Evolution')
st.altair_chart(gender_chart, use_container_width=True)
