import streamlit as st
import sqlite3

st.set_page_config(page_title="Timeline", layout="centered")

# Custom Fantasy Styling
st.markdown("""
    <style>
    /* Import fantasy header + rulebook body fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    /* Set page-wide font and text color */
    html, body, [class*="css"]  {
        font-family: 'Lora', serif !important;
        color: #000000 !important;
    }

    /* Container styling for better contrast */
    .stContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Use Cinzel for all headers (event titles, section headings) */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

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
for date, title, summary, full_description in events:
    st.header(title)
    st.write(date)

    with st.expander(f"Summary: {summary}"):
        st.write(full_description)
