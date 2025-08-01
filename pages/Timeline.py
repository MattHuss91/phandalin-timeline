
import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Timeline", layout="centered")

# Custom Fantasy Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        color: #000000 !important;
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }

    .stContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Phandalin Campaign Timeline")

conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Ensure the EventTimeline view exists
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

# Character filter
all_characters = events_df['people_involved'].str.split(', ').explode().dropna().unique()
selected_character = st.selectbox("Filter by character", ["All"] + sorted(all_characters.tolist()))

if selected_character != "All":
    events_df = events_df[events_df['people_involved'].str.contains(selected_character)]

# Date slider
labels = events_df['date_occurred'].tolist()
day_to_label = dict(zip(events_df['world_day'], events_df['date_occurred']))
label_to_day = {v: k for k, v in day_to_label.items()}

selected_start, selected_end = st.select_slider(
    "Select a date range",
    options=labels,
    value=(labels[0], labels[-1])
)

start_day = label_to_day[selected_start]
end_day = label_to_day[selected_end]

filtered_events = events_df[(events_df['world_day'] >= start_day) & (events_df['world_day'] <= end_day)]

# Display timeline
for _, row in filtered_events.iterrows():
    st.header(row['title'])
    st.write(f"{row['date_occurred']} — {row['location']}")
    st.markdown(f"**Summary:** {row['summary']}")
    st.write(row['full_description'])

    st.markdown("**People Involved:**")
    for character in row['people_involved'].split(', '):
        encoded_name = urllib.parse.quote(character)
        profile_url = f"/character_profiles?character={encoded_name}"
        st.markdown(f"- [{character}]({profile_url})")

conn.close()
