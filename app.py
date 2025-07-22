import sqlite3

import streamlit as st

st.title("The Heroes of Phandalin")
st.write("The box was just the start")
search_name = st.text_input("Search character name:")

st.title("Phandalin Campaign Timeline")

# Connect to database
conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Get event timeline
cursor.execute("""
    SELECT date_occurred, title 
    FROM CampaignEvents 
    ORDER BY world_day;
""")
events = cursor.fetchall()

# Display events
for title, date in events:
    st.subheader(title)
    st.write(date)

