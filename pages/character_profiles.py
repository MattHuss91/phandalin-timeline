import streamlit as st
import pandas as pd
from utils.db import query
from utils.ui import apply_global_styles, page_header, footer

# --- Streamlit page config ---
st.set_page_config(page_title="Loreweave • Characters", layout="centered")
apply_global_styles()
page_header("Characters")

# --- Get all characters for dropdown ---
characters = query("SELECT character_id, name FROM characters ORDER BY name ASC")
if not characters:
    st.info("No characters found in the database.")
    footer()
    st.stop()

char_dict = {c["name"]: c["character_id"] for c in characters}

# --- Character selection ---
selected_name = st.selectbox("Select a character", list(char_dict.keys()))
selected_id = char_dict[selected_name]

# --- Get selected character details ---
row = query("""
    SELECT name, type, status, bio, is_player, character_img
    FROM characters
    WHERE character_id = %s
""", (selected_id,))

if not row:
    st.warning("Character not found.")
    footer()
    st.stop()

char = row[0]

# --- Render character profile ---
st.markdown(f"## {char['name']}")
if char["type"]:
    st.markdown(f"**Type:** {char['type']}")
if char["status"]:
    st.markdown(f"**Status:** {char['status']}")

# Character image
if char["character_img"]:
    st.image(char["character_img"], width=None)  # compatible with older Streamlit

# Bio
if char["bio"]:
    st.markdown("### Biography")
    st.write(char["bio"])

# Is player?
if char["is_player"]:
    st.markdown("*Player Character*")
else:
    st.markdown("*Non-Player Character*")

footer()
