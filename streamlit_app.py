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
    st.subheader('Type of Medals and Sports Analysis')

    # Define dropdown selectors for season, year, and country
    #season_dropdown = st.selectbox('Select Season', ['summer', 'winter'])
    season_button = st.radio('Select Season', ['summer', 'winter'])
    year_dropdown = st.selectbox('Select Year', olympics['Year'].unique())
    country_dropdown = st.selectbox('Select Country', olympics['Country'].unique())

    st.subheader('Gender Evolution Analysis')


# Define a function to filter data based on selected filters
def filter_data(year, country, season):
    filtered_data = olympics[(olympics['Year'] == year) & (olympics['Country'] == country) & (olympics['Season'] == season)]
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
        height=400,
        title='Distribution of Medals by type in the Olympic games'
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
        height=400,
        title='Number of Sports per Country, Year, and Season'
    )
    return chart

# Define the function to update the visualization when filters change
def update():
    filtered_data = filter_data(year_dropdown, country_dropdown, season_dropdown)
    medal_chart = create_medal_chart(filtered_data)
    sport_chart = create_sport_chart(filtered_data)
    return medal_chart, sport_chart

# Initial update
medal_chart, sport_chart = update()

# Display charts in two columns
col1, col2 = st.columns(2)
with col1:
    st.subheader('Distribution of Medals per Type')
    st.altair_chart(medal_chart, use_container_width=True)
with col2:
    st.subheader('Distribution of Medals per Sport')
    st.altair_chart(sport_chart, use_container_width=True)

# Third charts

# Define dropdown selector for country
country_dropdown = alt.binding_select(options=olympics['Country'].unique().tolist())
country_selector = alt.selection_single(fields=['Country'], bind=country_dropdown, name='Select Country')

# Filter data for Summer and Winter Olympics
summer_data = olympics[olympics['Season'] == 'summer']
winter_data = olympics[olympics['Season'] == 'winter']

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

# Apply selector and transform the data based on the selected country for Summer Olympics
filtered_summer_chart = summer_chart.add_selection(
    country_selector
).transform_filter(
    country_selector
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

# Apply selector and transform the data based on the selected country for Winter Olympics
filtered_winter_chart = winter_chart.add_selection(
    country_selector
).transform_filter(
    country_selector
)

# Combine the two charts
combined_chart = alt.hconcat(filtered_summer_chart, filtered_winter_chart)

# Show the combined chart underneath the existing charts
st.subheader('Total Number of Medals by Gender Evolution')
st.write(combined_chart)
