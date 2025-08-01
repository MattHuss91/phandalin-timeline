
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Character Profiles", layout="centered")

# Styling
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
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Character Profiles")

# Connect to DB
conn = sqlite3.connect("dnd_campaign.db")

# Load character data
character_df = pd.read_sql_query("SELECT character_id, name, bio FROM characters ORDER BY name", conn)
character_names = character_df["name"].tolist()

# Query param linking
query_params = st.query_params
default_character = query_params.get("character", [""])[0]
index = character_names.index(default_character) if default_character in character_names else 0

selected_character = st.selectbox("Choose a character", character_names, index=index)
character_row = character_df[character_df["name"] == selected_character].iloc[0]
character_id = character_row["character_id"]

st.header(selected_character)
st.write("### Bio")
st.write(character_row["bio"])

# Load events
event_df = pd.read_sql_query(
    """
    SELECT ce.date_occurred, ce.title
    FROM characterappearances ca
    JOIN CampaignEvents ce ON ca.event_id = ce.event_id
    WHERE ca.character_id = ?
    ORDER BY ce.world_day
    """, conn, params=(character_id,)
)

# Show event list
if not event_df.empty:
    with st.expander("Events Involved"):
        for _, row in event_df.iterrows():
            st.markdown(f"- {row['date_occurred']}: {row['title']}")
else:
    st.write("No recorded events.")

conn.close()
