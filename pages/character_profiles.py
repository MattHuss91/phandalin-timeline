import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Character Profiles", layout="centered")

# --- Styling ---
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

st.title("Character Profiles")

# --- Load Data ---
conn = sqlite3.connect("dnd_campaign.db")
character_df = pd.read_sql_query("SELECT character_id, name, bio FROM characters ORDER BY name", conn)

# --- Query Params ---
query_params = st.query_params
character_id_str = query_params.get("character_id", [""])[0]

if character_id_str.isdigit():
    character_id = int(character_id_str)
    character_row = character_df[character_df["character_id"] == character_id]
    if character_row.empty:
        st.warning("Character not found in database.")
        character_id = None
    else:
        character_row = character_row.iloc[0]
        default_name = character_row["name"]
else:
    character_id = None
    default_name = None

# --- Character Selectbox ---
character_names = character_df["name"].tolist()

# Compute index for dropdown
try:
    index = character_names.index(default_name) if default_name else 0
except ValueError:
    index = 0

selected_character = st.selectbox(
    "Choose a character",
    character_names,
    index=index,
    key="character_select_box"
)

# --- Update Character Info from Dropdown ---
character_row = character_df[character_df["name"] == selected_character].iloc[0]
character_id = int(character_row["character_id"])

# --- Display Character Info ---
st.header(selected_character)
st.write("### Bio")
st.write(character_row["bio"])

# --- Load Related Events ---
event_df = pd.read_sql_query(
    """
    SELECT ce.date_occurred, ce.title
    FROM characterappearances ca
    JOIN CampaignEvents ce ON ca.event_id = ce.event_id
    WHERE ca.character_id = ?
    ORDER BY ce.world_day
    """, conn, params=(character_id,)
)

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
