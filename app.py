import sqlite3

import streamlit as st

st.title("The Heroes of Phandalin")
st.write("The box was just the start")

st.title("Phandalin Campaign Timeline")

# Connect to database
conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Query world_day and formatted date from the database
cursor.execute("""
    SELECT world_day, date_occurred
    FROM CampaignEvents
    ORDER BY world_day
""")
date_rows = cursor.fetchall()

# Create a mapping of world_day to readable label
day_to_label = {wd: label for wd, label in date_rows}

# Create a select_slider using labels only
labels = list(day_to_label.values())
selected_start, selected_end = st.select_slider(
    "Select a date range",
    options=labels,
    value=(labels[0], labels[-1])
)

# Reverse lookup to get the world_day numbers back
start_day = [wd for wd, label in day_to_label.items() if label == selected_start][0]
end_day = [wd for wd, label in day_to_label.items() if label == selected_end][0]

# Run the filtered query using world_day numbers
cursor.execute("""
    SELECT date_occurred, title, summary, full_description
    FROM CampaignEvents
    WHERE world_day BETWEEN ? AND ?
    ORDER BY world_day
""", (start_day, end_day))

events = cursor.fetchall()

# Display the events
for date, title, summary in events:
    st.write(date)
    st.subheader(title)
    st.write(summary)

with st.expander(f"More Detail: {title}"):
     st.write(full_description)
