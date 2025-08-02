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
character_names = character_df["name"].tolist()

# Get character from query params
query_params = st.query_params
default_character = query_params.get("character", [""])[0]

# Use query param to preselect dropdown
index = character_names.index(default_character) if default_character in character_names else 0

# Dropdown
selected_character = st.selectbox(
    "Choose a character",
    character_names,
    index=index,
    key="character_select_box"
)

# Normalize character name for safe matching
normalized_selection = selected_character.strip().replace("’", "'").lower()
character_df["normalized_name"] = character_df["name"].str.strip().str.replace("’", "'").str.lower()

# Lookup character by normalized name
character_row = character_df[character_df["normalized_name"] == normalized_selection]

if character_row.empty:
    st.error("Character not found.")
    st.stop()

character_row = character_row.iloc[0]
character_id = int(character_row["character_id"])

# DEBUG INFO
st.write("🟦 Selected character:", selected_character)
st.write("🟦 Character ID:", character_id, "| Type:", type(character_id))

# DEBUG: Check matching entries in characterappearances table
test_df = pd.read_sql_query(
    "SELECT * FROM characterappearances WHERE character_id = ?",
    conn,
    params=(character_id,)
)
st.write("🟩 Matching rows in characterappearances table:", test_df)

# Display character info
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

# DEBUG: Show event result
st.write("🟨 Matching events for character:", event_df)

# Display event list
if not event_df.empty:
    with st.expander("Events Involved"):
        for _, row in event_df.iterrows():
            event_title = row["title"]
            encoded_event = urllib.parse.quote(event_title)
            encoded_character = urllib.parse.quote(selected_character)

            st.markdown(f"- {row['date_occurred']}: [{event_title}](/?highlight={encoded_event}&from_character={encoded_character})")
else:
    st.warning("No recorded events.")

conn.close()
