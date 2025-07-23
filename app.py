import sqlite3

import streamlit as st

st.title("The Heroes of Phandalin")
st.write("The box was just the start")
search_name = st.text_input("Search character name:")

st.title("Phandalin Campaign Timeline")

# Connect to database
conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Get the min and max world_day values from the database
cursor.execute("SELECT MIN(world_day), MAX(world_day) FROM CampaignEvents")
min_day, max_day = cursor.fetchone()

# Create a slider for the player to choose a date range
start, end = st.slider("Select a date range", min_day, max_day, (min_day, max_day))

# Query events within that world_day range
cursor.execute("""
    SELECT date_occurred, title, summary
    FROM CampaignEvents
    WHERE world_day BETWEEN ? AND ?
    ORDER BY world_day
""", (start, end))

# Fetch and display results
events = cursor.fetchall()

for date, title, summary in events:
    st.write(date)
    st.subheader(title)
    st.write(summary)
