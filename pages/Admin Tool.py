import streamlit as st
import sqlite3
from datetime import datetime

# --- Carry log in details ---
st.set_page_config(page_title="Admin Tool", layout="centered")
user = st.session_state.get("username")

# --- CONNECT TO DATABASE ---
conn = sqlite3.connect("dnd_campaign.db")
c = conn.cursor()

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
    /* Force text inside button to white */
    div.stButton > button span {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    div.stButton > button:hover {
        background-color: #444444 !important;
        color: #ffffff !important;
    }
    html, body, .stApp, .stTextInput, .stTextArea, .stSelectbox, .stMarkdown, .stRadio, .stForm {
        color: #000000 !important;
    }

    label, h1, h2, h3, p, span, div, input, textarea {
        color: #000000 !important;
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

        c.execute("SELECT bio, is_player FROM characters WHERE character_id = ?", (char_id,))
        row = c.fetchone()
        default_bio, default_is_player = row

        with st.form("edit_character"):
            name = st.text_input("Character Name", value=selected_name)
            bio = st.text_area("Bio", value=default_bio)
            is_player = st.checkbox("Is Player?", value=bool(default_is_player))
            submit = st.form_submit_button("Save Changes")
            if submit:
                c.execute(
                    "UPDATE characters SET name = ?, bio = ?, is_player = ? WHERE character_id = ?",
                    (name, bio, int(is_player), char_id)
                )
                conn.commit()
                st.success(f"Character '{name}' updated.")
    else:
        with st.form("create_character"):
            name = st.text_input("Character Name")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            submit = st.form_submit_button("Create Character")
            if submit:
                c.execute(
                    "INSERT INTO characters (name, bio, is_player) VALUES (?, ?, ?)",
                    (name, bio, int(is_player))
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
            

st.markdown("---")
st.caption("Loreweave Admin Panel — Full Control")




