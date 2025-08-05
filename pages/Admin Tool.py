import os
import shutil
import streamlit as st
import sqlite3
from datetime import datetime

# Set paths for database
db_path = "/mnt/data/dnd_campaign.db"
src_path = "dnd_campaign.db"

# Ensure /mnt/data exists (persistent writable dir in Streamlit Cloud)
if not os.path.exists("/mnt/data"):
    os.makedirs("/mnt/data")

# Copy DB from app root to /mnt/data if not already there
if not os.path.exists(db_path):
    if os.path.exists(src_path):
        shutil.copy(src_path, db_path)
        st.write(f"Copied {src_path} to {db_path}")
    else:
        st.error("Source DB file not found!")
else:
    st.write("DB file already exists in /mnt/data/")

# Now connect to the copied DB in /mnt/data
conn = sqlite3.connect(db_path)
c = conn.cursor()

# --- Carry log in details ---
st.set_page_config(page_title="Admin Tool", layout="centered")
user = st.session_state.get("username")

# --- CONNECT TO DATABASE ---
import os

db_path = "/mnt/data/dnd_campaign.db"

# If the file doesn't exist, copy your local template version from the repo
if not os.path.exists(db_path):
    import shutil
    shutil.copy("dnd_campaign.db", db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    /* Background & font */
    .stApp {
        font-family: 'Lora', serif !important;
        color: #ffffff !important;
    }

    label {
        color: #ffffff !important;
        font-weight: bold;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
    }

    /* Input and textarea text */
    .stTextInput input,
    .stTextArea textarea {
        color: white !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] {
        color: white !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
    }

    /* Dropdown menu options */
    div[data-baseweb="menu"] div[role="option"] {
        color: white !important;
        background-color: rgba(0, 0, 0, 0.85) !important;
    }

    /* Dropdown hover effect */
    div[data-baseweb="menu"] div[role="option"]:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #333333 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
    }

    /* Form buttons */
    div.stForm button, div.stForm button span {
        color: white !important;
        background-color: #333333 !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
    }

    /* ✅ Radio button label text fix */
    div[data-baseweb="radio"] label > div:first-child {
        color: black !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATE SETTINGS ---
def parse_date(text_date):
    day_map = {"1st": 1, "2nd": 2, "3rd": 3, **{f"{i}th": i for i in range(4, 37)}}
    month_map = {
        "Verdanir": 1, "Emberfall": 2, "Duskwatch": 3, "Glimmerwane": 4,
        "Brightreach": 5, "Stormrest": 6, "Hollowshade": 7,
        "Deepmoor": 8, "Frostmere": 9, "Starwake": 10
    }
    try:
        parts = text_date.split()
        day = day_map.get(parts[0], 1)
        month = month_map.get(parts[1], 1)
        year = int(parts[2])
        world_day = (month - 1) * 36 + (day - 1)
        return day, month, year, world_day
    except Exception:
        return None, None, None, None
		
# --- GET ALL TABLE HELPER FUNCTION ---
def get_all(table, id_col, name_col):
    c.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    return c.fetchall()
	
# --- ADMIN CONTROL ---
if "user_role" not in st.session_state or st.session_state.user_role != "Admin":
    st.error("Access denied. Only Admin may use this tool")
    st.stop()
    
 # --- PAGE UI --- 
st.markdown("## Loreweave Admin Tool")

action = st.selectbox("What would you like to manage?", [
    "Character", "Event", "Location", "Faction", "Link character to event", "Link character to faction"
])

st.markdown("---")

# --- CHARACTER MANAGEMENT ---
if action == "Character":
    mode = st.radio("Action", ["Create new", "Edit existing"])

    if mode == "Edit existing":
        characters = get_all("characters", "character_id", "name")
        char_dict = {name: cid for cid, name in characters}
        selected_name = st.selectbox("Select Character", list(char_dict.keys()))
        char_id = char_dict[selected_name]

        c.execute("SELECT bio, type, status, is_player FROM characters WHERE character_id = ?", (char_id,))
        row = c.fetchone()
        default_bio, default_type, default_status, default_is_player = row

        with st.form("edit_character"):
            name = st.text_input("Character Name", value=selected_name)
            char_type = st.text_input("Type", value=default_type)
            status = st.text_input("Status", value=default_status)
            bio = st.text_area("Bio", value=default_bio)
            is_player = st.checkbox("Is Player?", value=bool(default_is_player))
            submit = st.form_submit_button("Save Changes")
            if submit:
                c.execute(
                    "UPDATE characters SET name = ?, type = ?, status = ?, bio = ?, is_player = ? WHERE character_id = ?",
                    (name, char_type, status, bio, int(is_player), char_id)
                )
                conn.commit()
                st.success(f"Character '{name}' updated.")

    else:
        with st.form("create_character"):
            name = st.text_input("Character Name")
            char_type = st.text_input("Type")
            status = st.text_input("Status")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            submit = st.form_submit_button("Create Character")
            if submit:
                c.execute(
                    "INSERT INTO characters (name, type, status, bio, is_player) VALUES (?, ?, ?, ?, ?)",
                    (name, char_type, status, bio, int(is_player))
                )
                conn.commit()
                st.success(f"Character '{name}' created.")

# --- EVENT MANAGEMENT ---
elif action == "Event":
    mode = st.radio("Action", ["Create new", "Edit existing"])

    
    locations = get_all("locations", "location_id", "name")
    loc_dict = {name: lid for lid, name in locations}
    reverse_loc_dict = {lid: name for name, lid in loc_dict.items()}

    if mode == "Edit existing":
        events = get_all("events", "event_id", "title")
        event_dict = {title: eid for eid, title in events}
        selected_title = st.selectbox("Select Event", list(event_dict.keys()))
        event_id = event_dict[selected_title]

        c.execute("""
            SELECT short_summary, long_description, date_occurred, location_id
            FROM events WHERE event_id = ?
        """, (event_id,))
        row = c.fetchone()
        default_summary, default_long, default_date, default_location_id = row

        # Preselect location name
        default_loc_name = reverse_loc_dict.get(default_location_id, list(loc_dict.keys())[0])

        with st.form("edit_event"):
            title = st.text_input("Event Title", value=selected_title)
            summary = st.text_area("Short Summary", value=default_summary)
            long_desc = st.text_area("Long Description", value=default_long)
            date_input = st.text_input("Date (e.g., '1st Verdanir 1452')", value=default_date)
            location_name = st.selectbox("Location", list(loc_dict.keys()), index=list(loc_dict.keys()).index(default_loc_name))
            location_id = loc_dict[location_name]

            submit = st.form_submit_button("Save Changes")
            if submit:
                day, month, year, world_day = parse_date(date_input)
                if None in (day, month, year, world_day):
                    st.error("Invalid date format.")
                else:
                    c.execute("""
                        UPDATE events
                        SET title = ?, short_summary = ?, long_description = ?, date_occurred = ?, day = ?, month = ?, year = ?, world_day = ?, location_id = ?
                        WHERE event_id = ?
                    """, (title, summary, long_desc, date_input, day, month, year, world_day, location_id, event_id))
                    conn.commit()
                    st.success(f"Event '{title}' updated.")

    else:
        with st.form("create_event"):
            title = st.text_input("Event Title")
            summary = st.text_area("Short Summary")
            long_desc = st.text_area("Long Description")
            date_input = st.text_input("Date (e.g., '1st Verdanir 1452')")
            location_name = st.selectbox("Location", list(loc_dict.keys()))
            location_id = loc_dict[location_name]

            submit = st.form_submit_button("Create Event")
            if submit:
                day, month, year, world_day = parse_date(date_input)
                if None in (day, month, year, world_day):
                    st.error("Invalid date format.")
                else:
                    c.execute("""
                        INSERT INTO events (title, short_summary, long_description, date_occurred, day, month, year, world_day, location_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (title, summary, long_desc, date_input, day, month, year, world_day, location_id))
                    conn.commit()
                    st.success(f"Event '{title}' created.")

# --- LOCATION MANAGEMENT ---
if action == "Location":
    mode = st.radio("Action", ["Create new", "Edit existing"])

    if mode == "Edit existing":
        locations = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locations}
        selected_name = st.selectbox("Select Location", list(loc_dict.keys()))
        loc_id = loc_dict[selected_name]

        c.execute("""
            SELECT name, region, description
            FROM locations WHERE location_id = ?
        """, (loc_id,))
        row = c.fetchone()
        default_name, default_region, default_description = row

        with st.form("edit_location"):
            name = st.text_input("Location Name", value=default_name)
            region = st.text_input("Region", value=default_region)
            description = st.text_area("Description", value=default_description)
            submit = st.form_submit_button("Save Changes")
            if submit:
                c.execute(
                    "UPDATE locations SET name = ?, region = ?, description = ? WHERE location_id = ?",
                    (name, region, description, loc_id)
                )
                conn.commit()
                st.success(f"Location '{name}' updated.")

    elif mode == "Create new":
        with st.form("create_location"):
            name = st.text_input("Location Name")
            region = st.text_input("Region")
            description = st.text_area("Description")
            submit = st.form_submit_button("Create Location")
            if submit:
                c.execute(
                    "INSERT INTO locations(name, region, description) VALUES (?, ?, ?)",
                    (name, region, description)
                )
                conn.commit()
                st.success(f"Location '{name}' created.")
                
# --- FACTION MANAGEMENT ---
if action == "Faction":
    mode = st.radio("Action", ["Create new", "Edit existing"])

    if mode == "Edit existing":
        factions = get_all("factions", "faction_id", "name")
        faction_dict = {name: fid for fid, name in factions}
        selected_name = st.selectbox("Select Faction", list(faction_dict.keys()))
        faction_id = faction_dict[selected_name]

        c.execute("""
            SELECT name, alignment, goals
            FROM factions WHERE faction_id = ?
        """, (faction_id,))
        row = c.fetchone()
        default_name, default_alignment, default_goals = row

        with st.form("edit_faction"):
            name = st.text_input("Faction Name", value=default_name)
            alignment = st.text_input("Alignment", value=default_alignment)
            goals = st.text_area("Goals", value=default_goals)
            submit = st.form_submit_button("Save Changes")
            if submit:
                c.execute(
                    "UPDATE factions SET name = ?, alignment = ?, goals = ? WHERE faction_id = ?",
                    (name, alignment, goals, faction_id)
                )
                conn.commit()
                st.success(f"Faction '{name}' updated.")

    elif mode == "Create new":
        with st.form("create_faction"):
            name = st.text_input("Faction Name")
            alignment = st.text_input("Alignment")
            goals = st.text_area("Goals")
            submit = st.form_submit_button("Create Faction")
            if submit:
                c.execute(
                    "INSERT INTO factions(name, alignment, goals) VALUES (?, ?, ?)",
                    (name, alignment, goals)
                )
                conn.commit()
                st.success(f"Faction '{name}' created.")


# --- CHARACTER EVENT LINKING ---
elif action == "Link character to event":
    characters = get_all("characters", "character_id", "name")
    events = get_all("events", "event_id", "title")
    char_dict = {name: cid for cid, name in characters}
    event_dict = {title: eid for eid, title in events}

    with st.form("link_char_event"):
        character = st.selectbox("Character", list(char_dict.keys()))
        event = st.selectbox("Event", list(event_dict.keys()))
        submit = st.form_submit_button("Link Character to Event")
        if submit:
            c.execute("INSERT INTO CharacterAppearances (character_id, event_id) VALUES (?, ?)",
                      (char_dict[character], event_dict[event]))
            conn.commit()
            st.success(f"{character} linked to '{event}'.")

# --- CHARACTER FACTION LINKING ---
elif action == "Link character to faction":
    characters = get_all("characters", "character_id", "name")
    factions = get_all("factions", "faction_id", "name")
    char_dict = {name: cid for cid, name in characters}
    faction_dict = {name: fid for fid, name in factions}

    with st.form("link_char_faction"):
        character = st.selectbox("Character", list(char_dict.keys()))
        faction = st.selectbox("Faction", list(faction_dict.keys()))
        submit = st.form_submit_button("Link Character to Faction")
        if submit:
            c.execute("INSERT INTO CharacterFactions (character_id, faction_id) VALUES (?, ?)",
                      (char_dict[character], faction_dict[faction]))
            conn.commit()
            st.success(f"{character} added to faction '{faction}'.")
            
if st.session_state.get("user_role") == "Admin":
    with open("/mnt/data/dnd_campaign.db", "rb") as f:
        st.download_button("⬇️ Download updated database", f, file_name="dnd_campaign.db")
	    
st.markdown("---")
st.caption("Loreweave Admin Panel — Full Control")






















