import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Character Profiles", layout="centered")

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
    </style>
""", unsafe_allow_html=True)

st.title("Character Profiles")

# Connect to database
conn = sqlite3.connect("dnd_campaign.db")
character_df = pd.read_sql_query("SELECT character_id, name, bio FROM characters ORDER BY name", conn)

# Get character ID from query param
query_params = st.query_params
character_id_str = query_params.get("character_id", [""])[0]

if character_id_str.isdigit():
    character_id = int(character_id_str)
else:
    st.error("Invalid or missing character_id.")
    st.stop()

# Get character row by ID
character_row = character_df[character_df["character_id"] == character_id]

if character_row.empty:
    st.error("Character not found.")
    st.stop()

character_row = character_row.iloc[0]
selected_character = character_row["name"]

# Dropdown for manual override (optional)
character_names = character_df["name"].tolist()
selected_character = st.selectbox(
    "Choose a character",
    character_names,
    index=character_df[character_df["character_id"] == character_id].index[0],
    key="character_select_box"
)

# Update ID from dropdown (if user changes manually)
character_row = character_df[character_df["name"] == selected_character].iloc[0]
character_id = int(character_row["character_id"])

# Display bio
st.header(selected_character)
st.write("### Bio")
st.write(character_row["bio"])

# Load related events
event_df = pd.read_sql_query(
    """
    SELECT ce.date_occurred, ce.title
    FROM characterappearances ca
    JOIN CampaignEvents ce ON ca.event_id = ce.event_id
    WHERE ca.character_id = ?
    ORDER BY ce.world_day
    """, conn, params=(character_id,)
)

# Display event list
if not event_df.empty:
    with st.expander("Events Involved"):
        for _, row in event_df.iterrows():
            event_title = row["title"]
            encoded_event = urllib.parse.quote(event_title)
            encoded_character_id = str(character_id)
            st.markdown(
                f"- {row['date_occurred']}: "
                f"[{event_title}](/?highlight={encoded_event}&from_character_id={encoded_character_id})"
            )
else:
    st.warning("No recorded events.")

conn.close()
