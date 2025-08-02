import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Timeline", layout="centered")

# Get query params
query_params = st.query_params
highlight_event = query_params.get("highlight", [""])[0]
from_character = query_params.get("from_character", [""])[0]

# Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    .stApp {
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Lora', serif !important;
        color: #000000 !important;
    }

    .stContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
    }

    .stSelectbox label,
    .stSlider label {
        color: #000000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Phandalin Campaign Timeline")

# Connect to DB
conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Ensure view exists
cursor.executescript("""
DROP VIEW IF EXISTS EventTimeline;
CREATE VIEW EventTimeline AS
SELECT 
    ce.event_id,
    ce.title,
    ce.date_occurred,
    ce.summary,
    ce.full_description,
    ce.day,
    ce.month,
    ce.year,
    ce.world_day,
    l.name AS location,
    GROUP_CONCAT(c.name, ', ') AS people_involved
FROM CampaignEvents ce
LEFT JOIN characterappearances ca ON ce.event_id = ca.event_id
LEFT JOIN characters c ON ca.character_id = c.character_id
LEFT JOIN Locations l ON ce.location_id = l.location_id
GROUP BY ce.event_id;
""")

events_df = pd.read_sql_query("SELECT * FROM EventTimeline ORDER BY world_day", conn)

# Filter for highlighted event (if passed in URL)
if highlight_event:
    events_df = events_df[events_df["title"] == highlight_event]

# Back to character link
if from_character:
    encoded_name = urllib.parse.quote(from_character)
    st.markdown(f"[← Back to {from_character}](/character_profiles?character={encoded_name})")

# Only show filters if not in highlight mode
if not highlight_event:
    # Character filter
    all_characters = events_df['people_involved'].str.split(', ').explode().dropna().unique()
    selected_character = st.selectbox("Filter by character", ["All"] + sorted(all_characters.tolist()))

    if selected_character != "All":
        events_df = events_df[events_df['people_involved'].str.contains(selected_character)]

    # Slider filter
    labels = events_df['date_occurred'].tolist()
    day_to_label = dict(zip(events_df['world_day'], events_df['date_occurred']))
    label_to_day = {v: k for k, v in day_to_label.items()}
    selected_start, selected_end = st.select_slider("Select a date range", options=labels, value=(labels[0], labels[-1]))
    start_day = label_to_day[selected_start]
    end_day = label_to_day[selected_end]

    events_df = events_df[(events_df['world_day'] >= start_day) & (events_df['world_day'] <= end_day)]

# Display events
for _, row in events_df.iterrows():
    st.header(row['title'])
    st.write(f"{row['date_occurred']} — {row['location']}")
    st.markdown(f"**Summary:** {row['summary']}")
    st.write(row['full_description'])

    st.markdown("**People Involved:**")
    for character in row['people_involved'].split(', '):
        encoded_name = urllib.parse.quote(character)
        st.markdown(f"- [{character}](/character_profiles?character={encoded_name})")

conn.close()
