import streamlit as st
import sqlite3
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Admin Tool", layout="centered")

# --- Database Connection ---
DB_FILE = "dnd_campaign.db"  # must be in the repo root
try:
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
except sqlite3.Error as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# --- Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

.stApp {
    font-family: 'Lora', serif !important;
    color: #ffffff !important;
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
label, .stSelectbox label, .stRadio label { 
    color: #ffffff !important; 
    font-weight: bold; 
}

/* Inputs/TextAreas */
.stTextInput input,
.stTextArea textarea {
    color: white !important;
    background-color: rgba(0, 0, 0, 0.6) !important;
}

/* Selectbox */
div[data-baseweb="select"] { 
    color: white !important; 
    background-color: rgba(0, 0, 0, 0.6) !important; 
}
div[data-baseweb="menu"] div[role="option"] {
    color: white !important;
    background-color: rgba(0, 0, 0, 0.85) !important;
}
div[data-baseweb="menu"] div[role="option"]:hover {
    background-color: rgba(255,255,255,0.2) !important;
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
div.stForm button, div.stForm button span {
    color: white !important;
    background-color: #333333 !important;
    font-weight: bold !important;
    font-family: 'Cinzel', serif !important;
}
</style>
""", unsafe_allow_html=True)

# --- Authentication ---
if st.session_state.get("user_role") != "Admin":
    st.error("Access denied. Only Admin may use this tool.")
    st.stop()

# --- Utility Functions ---
def parse_date(text_date):
    day_map = {f"{i}th": i for i in range(1, 37)}
    day_map.update({"1st":1, "2nd":2, "3rd":3})
    month_map = {
        "Verdanir":1, "Emberfall":2, "Duskwatch":3, "Glimmerwane":4,
        "Brightreach":5, "Stormrest":6, "Hollowshade":7,
        "Deepmoor":8, "Frostmere":9, "Starwake":10
    }
    try:
        parts = text_date.split()
        day = day_map.get(parts[0])
        month = month_map.get(parts[1])
        year = int(parts[2])
        world_day = (month - 1) * 36 + (day - 1)
        return day, month, year, world_day
    except:
        return None, None, None, None

def get_all(table, id_col, name_col):
    c.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    return c.fetchall()

# --- Page Header ---
st.markdown("## Loreweave Admin Tool")
action = st.selectbox("What would you like to manage?", [
    "Character", "Event", "Location", "Faction",
    "Link character to event", "Link character to faction"
])
st.markdown("---")

# --- CHARACTER MANAGEMENT ---
if action == "Character":
    mode = st.radio("Action", ["Create new", "Edit existing"])
    if mode == "Edit existing":
        chars = get_all("characters", "character_id", "name")
        char_dict = {name: cid for cid, name in chars}
        sel = st.selectbox("Select Character", list(char_dict.keys()))
        cid = char_dict[sel]
        c.execute("SELECT name, type, status, bio, is_player FROM characters WHERE character_id = ?", (cid,))
        name0, type0, status0, bio0, is_player0 = c.fetchone()
        with st.form("edit_char"):
            name = st.text_input("Name", value=name0)
            ctype = st.text_input("Type", value=type0)
            status = st.text_input("Status", value=status0)
            bio = st.text_area("Bio", value=bio0)
            is_player = st.checkbox("Is Player?", value=bool(is_player0))
            if st.form_submit_button("Save Changes"):
                c.execute(
                    "UPDATE characters SET name=?, type=?, status=?, bio=?, is_player=? WHERE character_id=?",
                    (name, ctype, status, bio, int(is_player), cid)
                )
                conn.commit()
                st.success(f"Character '{name}' updated.")
    else:
        with st.form("create_char"):
            name = st.text_input("Name")
            ctype = st.text_input("Type")
            status = st.text_input("Status")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            if st.form_submit_button("Create Character"):
                c.execute(
                    "INSERT INTO characters(name,type,status,bio,is_player) VALUES (?,?,?,?,?)",
                    (name, ctype, status, bio, int(is_player))
                )
                conn.commit()
                st.success(f"Character '{name}' created.")

# --- EVENT MANAGEMENT ---
elif action == "Event":
    mode = st.radio("Action", ["Create new", "Edit existing"])
    locs = get_all("locations", "location_id", "name")
    loc_dict = {name: lid for lid, name in locs}
    rev_loc = {lid: name for name, lid in loc_dict.items()}
    if mode == "Edit existing":
        evs = get_all("campaignevents", "event_id", "title")
        ev_dict = {title: eid for eid, title in evs}
        sel = st.selectbox("Select Event", list(ev_dict.keys()))
        eid = ev_dict[sel]
        c.execute("SELECT title, summary, full_description, date_occurred, location_id FROM campaignevents WHERE event_id = ?", (eid,))
        t0, s0, l0, d0, loc0 = c.fetchone()
        idx = list(loc_dict.keys()).index(rev_loc.get(loc0, "")) if loc0 in rev_loc else 0
        with st.form("edit_event"):
            title = st.text_input("Title", value=t0)
            summary = st.text_area("Summary", value=s0)
            longd = st.text_area("Description", value=l0)
            date_input = st.text_input("Date (e.g. '1st Verdanir 1452')", value=d0)
            loc_name = st.selectbox("Location", list(loc_dict.keys()), index=idx)
            loc_id = loc_dict[loc_name]
            if st.form_submit_button("Save Changes"):
                day, m, y, wd = parse_date(date_input)
                if None in (day, m, y, wd):
                    st.error("Invalid date.")
                else:
                    c.execute(
                        "UPDATE campaignevents SET title=?, short_summary=?, long_description=?, date_occurred=?, day=?, month=?, year=?, world_day=?, location_id=? WHERE event_id=?",
                        (title, summary, longd, date_input, day, m, y, wd, loc_id, eid)
                    )
                    conn.commit()
                    st.success(f"Event '{title}' updated.")
    else:
        with st.form("create_event"):
            title = st.text_input("Title")
            summary = st.text_area("Summary")
            longd = st.text_area("Description")
            date_input = st.text_input("Date (e.g. '1st Verdanir 1452')")
            loc_name = st.selectbox("Location", list(loc_dict.keys()))
            loc_id = loc_dict[loc_name]
            if st.form_submit_button("Create Event"):
                day, m, y, wd = parse_date(date_input)
                if None in (day, m, y, wd):
                    st.error("Invalid date.")
                else:
                    c.execute(
                        "INSERT INTO campaigncampaignevents(title,short_summary,long_description,date_occurred,day,month,year,world_day,location_id) VALUES (?,?,?,?,?,?,?,?,?)",
                        (title, summary, longd, date_input, day, m, y, wd, loc_id)
                    )
                    conn.commit()
                    st.success(f"Event '{title}' created.")

# --- LOCATION MANAGEMENT ---
elif action == "Location":
    mode = st.radio("Action", ["Create new", "Edit existing"])
    if mode == "Edit existing":
        locs = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locs}
        sel = st.selectbox("Select Location", list(loc_dict.keys()))
        lid = loc_dict[sel]
        c.execute("SELECT name, region, description FROM locations WHERE location_id=?", (lid,))
        n0, r0, d0 = c.fetchone()
        with st.form("edit_loc"):
            name = st.text_input("Name", value=n0)
            region = st.text_input("Region", value=r0)
            desc = st.text_area("Description", value=d0)
            if st.form_submit_button("Save Changes"):
                c.execute("UPDATE locations SET name=?, region=?, description=? WHERE location_id=?", (name, region, desc, lid))
                conn.commit()
                st.success(f"Location '{name}' updated.")
    else:
        with st.form("create_loc"):
            name = st.text_input("Name")
            region = st.text_input("Region")
            desc = st.text_area("Description")
            if st.form_submit_button("Create Location"):
                c.execute("INSERT INTO locations(name,region,description) VALUES (?,?,?)", (name, region, desc))
                conn.commit()
                st.success(f"Location '{name}' created.")

# --- FACTION MANAGEMENT ---
elif action == "Faction":
    mode = st.radio("Action", ["Create new", "Edit existing"])
    if mode == "Edit existing":
        facs = get_all("factions", "faction_id", "name")
        fac_dict = {name: fid for fid, name in facs}
        sel = st.selectbox("Select Faction", list(fac_dict.keys()))
        fid = fac_dict[sel]
        c.execute("SELECT name, alignment, goals FROM factions WHERE faction_id=?", (fid,))
        n0, a0, g0 = c.fetchone()
        with st.form("edit_fac"):
            name = st.text_input("Name", value=n0)
            align = st.text_input("Alignment", value=a0)
            goals = st.text_area("Goals", value=g0)
            if st.form_submit_button("Save Changes"):
                c.execute("UPDATE factions SET name=?, alignment=?, goals=? WHERE faction_id=?", (name, align, goals, fid))
                conn.commit()
                st.success(f"Faction '{name}' updated.")
    else:
        with st.form("create_fac"):
            name = st.text_input("Name")
            align = st.text_input("Alignment")
            goals = st.text_area("Goals")
            if st.form_submit_button("Create Faction"):
                c.execute("INSERT INTO factions(name,alignment,goals) VALUES (?,?,?)", (name, align, goals))
                conn.commit()
                st.success(f"Faction '{name}' created.")

# --- CHARACTER ↔ EVENT LINKING ---
elif action == "Link character to event":
    chars = get_all("characters", "character_id", "name")
    evs = get_all("campaignevents", "event_id", "title")
    char_dict = {name: cid for cid, name in chars}
    ev_dict = {title: eid for eid, title in evs}
    with st.form("link_ce"):
        character = st.selectbox("Character", list(char_dict.keys()))
        event = st.selectbox("Event", list(ev_dict.keys()))
        if st.form_submit_button("Link"):
            c.execute("INSERT INTO CharacterAppearances(character_id,event_id) VALUES(?,?)",
                      (char_dict[character], ev_dict[event]))
            conn.commit()
            st.success(f"{character} linked to '{event}'.")

# --- CHARACTER ↔ FACTION LINKING ---
elif action == "Link character to faction":
    chars = get_all("characters", "character_id", "name")
    facs = get_all("factions", "faction_id", "name")
    char_dict = {name: cid for cid, name in chars}
    fac_dict = {name: fid for fid, name in facs}
    with st.form("link_cf"):
        character = st.selectbox("Character", list(char_dict.keys()))
        faction = st.selectbox("Faction", list(fac_dict.keys()))
        if st.form_submit_button("Link"):
            c.execute("INSERT INTO CharacterFactions(character_id,faction_id) VALUES(?,?)",
                      (char_dict[character], fac_dict[faction]))
            conn.commit()
            st.success(f"{character} added to '{faction}' faction.")

# --- Download Button ---
with open(DB_FILE, "rb") as f:
    st.download_button(
        label="⬇️ Download updated database",
        data=f,
        file_name="dnd_campaign.db",
        mime="application/octet-stream"
    )

st.markdown("---")
st.caption("Loreweave Admin Panel — Full Control")






