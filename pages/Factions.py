import streamlit as st
import psycopg2
import pandas as pd
import urllib.parse

# --- Streamlit config ---
st.set_page_config(page_title="Factions", layout="centered")
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
st.markdown("""
    <div style='text-align: center; margin-top: -20px;'>
        <img src='https://i.imgur.com/WEGvkz8.png' style='width: 200px; margin-bottom: -10px;' />
        <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>Factions</h1>
    </div>
""", unsafe_allow_html=True)

# --- Connect to Supabase ---
try:
    conn = psycopg2.connect(
        host=st.secrets["db_host"],
        dbname=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        port=st.secrets["port"],
        sslmode="require"
    )
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# --- Load Faction data ---
faction_df = pd.read_sql_query("SELECT faction_id, name, alignment, goals FROM factions ORDER BY name", conn)#

# --- Faction dropdown ---
faction_name = faction_df["name"].tolist()


selected_faction = st.selectbox("Choose a Faction", faction_name)
faction_row = faction_df[faction_df["name"] == selected_faction].iloc[0]
faction_id = int(faction_row["faction_id"])

# --- Display Faction Data ---
st.header(selected_faction)
st.write("### Bio")
st.write(faction_row["goals"])

# --- Related Characters ---
try:
    character_df = pd.read_sql_query("""
        SELECT ch.character_id, ch.name
        FROM characters ch
        JOIN characterfaction cf ON ch.character_id = cf.character_id
        WHERE cf.faction_id = %s
    """, conn, params=(faction_id,))
except Exception as e:
    st.error(f"Failed to fetch related factions: {e}")
    character_df = pd.DataFrame()

conn.close()

# --- Display Events ---
if not character_df.empty:
    with st.expander("Members"):
        for _, row in character_df.iterrows():
            st.markdown(f"- {row['name']}")
else:
    st.warning("No Members")

encoded_name = urllib.parse.quote(row["name"])
st.markdown(f"- [{row['name']}](Character_Profile.py?name={encoded_name})")

