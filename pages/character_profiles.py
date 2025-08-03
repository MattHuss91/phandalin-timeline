import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Character Profiles", layout="centered")
user = st.session_state.get("username")

# --- Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    html, body, .stApp, .block-container {
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Lora', serif !important;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        color: #000000;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        color: #000000 !important;
    }

    label, .stTextInput label, .stTextArea label {
        color: #000000 !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
    }

    textarea, div[data-baseweb="textarea"] textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-family: 'Lora', serif !important;
    }

    button[role="button"] {
        background-color: #333333 !important;
        color: #ffffff !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
    }

    button[role="button"]:hover {
        background-color: #444444 !important;
        color: #ffffff !important;
    }

    summary {
        color: #000000 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: bold !important;
    }

    .markdown-text-container, .stMarkdown, .stMarkdown p {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("Character Profiles")

# --- Load character data ---
conn = sqlite3.connect("dnd_campaign.db")
character_df = pd.read_sql_query("SELECT character_id, name, bio, editable_by FROM characters ORDER BY name", conn)

# --- Get character ID from URL ---
query_params = st.query_params
character_id_str = query_params.get("character_id", [""])[0]

if character_id_str.isdigit():
    character_id = int(character_id_str)
    character_row = character_df[character_df["character_id"] == character_id]
    if character_row.empty:
        st.warning("Character not found.")
        character_id = None
    else:
        character_row = character_row.iloc[0]
        default_name = character_row["name"]
else:
    character_id = None
    default_name = None

# --- Character dropdown ---
character_names = character_df["name"].tolist()
try:
    index = character_names.index(default_name) if default_name else 0
except ValueError:
    index = 0

selected_character = st.selectbox("Choose a character", character_names, index=index)
character_row = character_df[character_df["name"] == selected_character].iloc[0]
character_id = int(character_row["character_id"])
editable_by = character_row["Editable by"]

# --- Display Bio ---
st.header(selected_character)
st.write("### Bio")
st.write(character_row["bio"])

# --- Permissions Check ---
if user == "Admin":
    st.info("You are logged in as Admin. You can edit any character.")
    can_edit = True
elif user == editable_by:
    st.info(f"You are logged in as {user}, and you are allowed to edit this character.")
    can_edit = True
elif user:
    st.warning(f"You are logged in as {user}, but you cannot edit this character.")
    can_edit = False
else:
    can_edit = False

# --- Edit Bio ---
if can_edit:
    with st.expander("Edit Bio"):
        with st.form("edit_bio_form"):
            new_bio = st.text_area("Edit Bio", character_row["bio"], height=200)
            submitted = st.form_submit_button("Save Changes")

        if submitted and new_bio != character_row["bio"]:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE characters SET bio = ? WHERE character_id = ?", (new_bio, character_id))
                conn.commit()
                st.success("Bio updated successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating bio: {e}")

# --- Related Events ---
event_df = pd.read_sql_query("""
    SELECT ce.date_occurred, ce.title
    FROM characterappearances ca
    JOIN CampaignEvents ce ON ca.event_id = ce.event_id
    WHERE ca.character_id = ?
    ORDER BY ce.world_day
""", conn, params=(character_id,))
conn.close()

if not event_df.empty:
    with st.expander("Events Involved"):
        for _, row in event_df.iterrows():
            event_title = row["title"]
            encoded_event = urllib.parse.quote(event_title)
            st.markdown(f"- {row['date_occurred']}: [{event_title}](/?highlight={encoded_event}&from_character_id={character_id})")
else:
    st.warning("No recorded events.")
