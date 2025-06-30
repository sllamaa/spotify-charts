
import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium

# Load the entire dataset to get all countries
def load_full_data(filepath):
    return pd.read_csv(filepath)

# Load the entire dataset to get the full list of countries
full_data = load_full_data('df_withmonths.csv')

# Then, subset the data for other operations
def load_data(filepath, nrows=500):
    return pd.read_csv(filepath, nrows=nrows)

# Load the data (only 500 rows)
data = load_data('df_withmonths.csv')

# Optimize Data Types (Optional)
def optimize_data(df):
    df['month'] = df['month'].astype('category')
    df['trend'] = df['trend'].astype('category')
    df['artist'] = df['artist'].astype('category')
    df['region'] = df['region'].astype('category')  # Assuming 'region' represents the country
    return df

data = optimize_data(data)
full_data = optimize_data(full_data)

# Convert the unique values to a list
country_list = full_data["region"].unique().tolist()

# Streamlit Sidebar Filters
st.sidebar.header("Filters")

# Country filter
country = st.sidebar.selectbox("Select Country", options=sorted(country_list))  # Sorting for better usability

# Filter the data by the selected country
filtered_data = data[data["region"] == country]

# Convert the unique artist and trend values to a list
filtered_artist_list = filtered_data["artist"].unique().tolist()
filtered_trend_list = filtered_data["trend"].unique().tolist()

# Artist and Trend filters based on filtered country data
artist = st.sidebar.multiselect("Select Artist", options=sorted(filtered_artist_list), default=filtered_artist_list)
trend = st.sidebar.multiselect("Select Trend", options=filtered_trend_list, default=filtered_trend_list)

# Further filter the data by the selected artist and trend
filtered_data = filtered_data[(filtered_data["artist"].isin(artist)) & (filtered_data["trend"].isin(trend))]

# Display Data Table
st.write(f"## Spotify Top Tracks in {country}")
st.dataframe(filtered_data.head(100))  # Display only the first 100 rows

# Visualizations
# Bar Chart: Rank Distribution by Artist
st.write("## Rank Distribution by Artist")
rank_chart = alt.Chart(filtered_data).mark_bar().encode(
    x='artist:N',
    y='rank:Q',
    color='artist:N',
    tooltip=['title', 'rank', 'streams']
).interactive()
st.altair_chart(rank_chart, use_container_width=True)


# Pie Chart: Trend Proportion
st.write("## Trend Proportion")
trend_chart = alt.Chart(filtered_data).mark_arc().encode(
    theta=alt.Theta(field="streams", type="quantitative"),
    color=alt.Color(field="trend", type="nominal"),
    tooltip=['trend', 'streams']
).interactive()
st.altair_chart(trend_chart, use_container_width=True)

# Display Links to Spotify Tracks
st.write("## Spotify Links")
for i, row in filtered_data.iterrows():
    st.write(f"[{row['title']}]({row['url']}) by {row['artist']}")

