
import streamlit as st
import psycopg2
from datetime import datetime

st.set_page_config(page_title="Admin Tool", layout="centered")

# --- Database connection ---
try:
    conn = psycopg2.connect(
        host=st.secrets["db_host"],
        dbname=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        port=st.secrets["port"],
        sslmode="require"
    )
    c = conn.cursor()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# --- Styling ---
st.markdown("""<style>/* Add custom CSS here if needed */</style>""", unsafe_allow_html=True)

# --- Access control ---
if st.session_state.get("username") != "Admin":
    st.error("Access denied. Only Admins can access this page.")
    st.stop()

# --- Utility Functions ---
def parse_custom_date(date_str):
    month_map = {
        'Verdanir': 1,
        'Emberfall': 2,
        'Duskwatch': 3,
        'Glimmerwane': 4,
        'Brightreach': 5,
        'Stormrest': 6,
        'Hollowshade': 7,
        'Deepmoor': 8,
        'Frostmere': 9,
        'Starwake': 10
    }

    try:
        parts = date_str.strip().split(" ")
        day = int(parts[0].replace("st", "").replace("nd", "").replace("rd", "").replace("th", ""))
        month = month_map.get(parts[1], 0)
        year = int(parts[2].replace("AF", "").strip())

        world_day = (year * 360) + ((month - 1) * 36) + (day - 1)
        return day, month, year, world_day
    except Exception as e:
        st.error(f"Failed to parse date '{date_str}': {e}")
        return None, None, None, None
def get_all(table, id_col, name_col):
    c.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    return c.fetchall()

# --- Main interface ---
st.markdown("""
    <div style='text-align: center; margin-top: -20px;'>
        <img src='https://i.imgur.com/YBozTrh.png' style='width: 200px; margin-bottom: -10px;' />
        <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>Admin Tool</h1>
    </div>
""", unsafe_allow_html=True)
mode = st.sidebar.selectbox("What would you like to manage?", [
    "Characters", "Events", "Locations", "Factions", "Link Character to Event", "Link Character to Faction"])

# --- Characters ---
if mode == "Characters":
    submode = st.radio("Action", ["Create", "Edit"])
    if submode == "Edit":
        characters = get_all("characters", "character_id", "name")
        char_dict = {name: cid for cid, name in characters}
        selected = st.selectbox("Select Character", list(char_dict.keys()))
        cid = char_dict[selected]
        c.execute("SELECT name, type, status, bio, is_player FROM characters WHERE character_id = %s", (cid,))
        row = c.fetchone()
        with st.form("edit_char"):
            name = st.text_input("Name", value=row[0])
            ctype = st.text_input("Type", value=row[1])
            status = st.text_input("Status", value=row[2])
            bio = st.text_area("Bio", value=row[3])
            is_player = st.checkbox("Is Player?", value=row[4])
            if st.form_submit_button("Update"):
                c.execute("UPDATE characters SET name=%s, type=%s, status=%s, bio=%s, is_player=%s WHERE character_id = %s",
                          (name, ctype, status, bio, is_player, cid))
                conn.commit()
                st.success("Character updated.")
    else:
        with st.form("create_char"):
            name = st.text_input("Name")
            ctype = st.text_input("Type")
            status = st.text_input("Status")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            if st.form_submit_button("Create"):
                c.execute("INSERT INTO characters (name, type, status, bio, is_player) VALUES (%s, %s, %s, %s, %s)",
                          (name, ctype, status, bio, is_player))
                conn.commit()
                st.success("Character created.")
# Events
elif mode == "Events":
    submode = st.radio("Action", ["Create", "Edit"])

    # --- EDIT MODE ---
    if submode == "Edit":
        # Get events and locations
        events = get_all("campaignevents", "event_id", "title")
        event_dict = {name: eid for eid, name in events}

        locs = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locs}
        reverse_loc_dict = {lid: name for name, lid in loc_dict.items()}

        selected = st.selectbox("Select Event", list(event_dict.keys()))
        eid = event_dict[selected]

        c.execute("""
            SELECT title, date_occurred, location_id, summary, full_description
            FROM campaignevents
            WHERE event_id = %s
        """, (eid,))
        row = c.fetchone()

        with st.form("edit_event"):
            title = st.text_input("Title", value=row[0])
            date_occurred = st.text_input("Date Occurred", value=row[1])

            current_loc_name = reverse_loc_dict.get(row[2])
            loc = st.selectbox(
                "Location",
                list(loc_dict.keys()),
                index=list(loc_dict.keys()).index(current_loc_name) if current_loc_name else 0
            )

            summary = st.text_area("Summary", value=row[3])
            full_description = st.text_area("Full Description", value=row[4])

            if st.form_submit_button("Update"):
                day, month, year, world_day = parse_custom_date(date_occurred)

                c.execute("""
                    UPDATE campaignevents
                    SET title = %s,
                        date_occurred = %s,
                        location_id = %s,
                        summary = %s,
                        full_description = %s,
                        day = %s,
                        month = %s,
                        year = %s,
                        world_day = %s
                    WHERE event_id = %s
                """, (
                    title,
                    date_occurred,
                    loc_dict[loc],  
                    summary,
                    full_description,
                    day,
                    month,
                    year,
                    world_day,
                    eid
                ))
                conn.commit()
                st.success("Event updated.")

    # --- CREATE MODE ---
    else:
        locs = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locs}

        with st.form("create_event"):
            title = st.text_input("Title")
            date_occurred = st.text_input("Date Occurred (e.g., 4th Verdanir 1041)")
            loc = st.selectbox("Location", list(loc_dict.keys()))  
            summary = st.text_area("Summary")
            full_description = st.text_area("Full Description")

            if st.form_submit_button("Create"):
                day, month, year, world_day = parse_custom_date(date_occurred)

                try:
                    c.execute("""
                        INSERT INTO campaignevents 
                            (title, date_occurred, location_id, summary, full_description, day, month, year, world_day)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        title,
                        date_occurred,
                        loc_dict[loc],  
                        summary,
                        full_description,
                        day,
                        month,
                        year,
                        world_day
                    ))
                    conn.commit()
                    st.success("Event created.")
                except Exception as e:
                    st.error(f"Error creating event: {e}")


# --- Locations ---
elif mode == "Locations":
    submode = st.radio("Action", ["Create", "Edit"])
    if submode == "Edit":
        locs = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locs}
        selected = st.selectbox("Select Location", list(loc_dict.keys()))
        lid = loc_dict[selected]
        c.execute("SELECT name, region, description FROM locations WHERE location_id = %s", (lid,))
        row = c.fetchone()
        with st.form("edit_loc"):
            name = st.text_input("Name", value=row[0])
            reg = st.text_input("Region", value=row[1])
            desc = st.text_area("Description", value=row[2])
            if st.form_submit_button("Update"):
                c.execute("UPDATE locations SET name = %s, region = %s, description = %s WHERE location_id = %s",
                          (name, reg, desc, lid))
                conn.commit()
                st.success("Location updated.")
    else:
        with st.form("create_loc"):
            name = st.text_input("Name")
            reg = st.text_input("Region")
            desc = st.text_area("Description")
            if st.form_submit_button("Create"):
                c.execute("INSERT INTO locations (name, region, description) VALUES (%s, %s, %s)", (name, reg, desc))
                conn.commit()
                st.success("Location created.")

# --- Factions ---
elif mode == "Factions":
    submode = st.radio("Action", ["Create", "Edit"])
    if submode == "Edit":
        factions = get_all("factions", "faction_id", "name")
        fac_dict = {name: fid for fid, name in factions}
        selected = st.selectbox("Select Faction", list(fac_dict.keys()))
        fid = fac_dict[selected]
        c.execute("SELECT name, alignment, goals FROM factions WHERE faction_id = %s", (fid,))
        row = c.fetchone()
        with st.form("edit_faction"):
            name = st.text_input("Name", value=row[0])
            ali = st.text_area("Allignment", value=row[1])
            desc = st.text_area("Description", value=row[2])
            if st.form_submit_button("Update"):
                c.execute("UPDATE factions SET name = %s, alignment = %s, goals = %s WHERE faction_id = %s",
                          (name, ali, desc, fid))
                conn.commit()
                st.success("Faction updated.")
    else:
        with st.form("create_faction"):
            name = st.text_input("Name")
            ali = st.text_input("Alignment")
            desc = st.text_area("Description")
            if st.form_submit_button("Create"):
                c.execute("INSERT INTO factions (name, alignment, goals) VALUES (%s, %s, %s)", (name, ali, desc))
                conn.commit()
                st.success("Faction created.")

# --- Link Character to Event ---
elif mode == "Link Character to Event":
    chars = get_all("characters", "character_id", "name")
    events = get_all("campaignevents", "event_id", "title")
    char_dict = {name: cid for cid, name in chars}
    event_dict = {title: eid for eid, title in events}
    with st.form("link_char_event"):
        char = st.selectbox("Character", list(char_dict.keys()))
        event = st.selectbox("Event", list(event_dict.keys()))
        if st.form_submit_button("Link"):
            c.execute("INSERT INTO characterappearances (character_id, event_id) VALUES (%s, %s)",
                      (char_dict[char], event_dict[event]))
            conn.commit()
            st.success(f"Linked {char} to {event}")

# --- Link Character to Faction ---
elif mode == "Link Character to Faction":
    chars = get_all("characters", "character_id", "name")
    factions = get_all("factions", "faction_id", "name")
    char_dict = {name: cid for cid, name in chars}
    fac_dict = {name: fid for fid, name in factions}
    with st.form("link_char_faction"):
        char = st.selectbox("Character", list(char_dict.keys()))
        fac = st.selectbox("Faction", list(fac_dict.keys()))
        if st.form_submit_button("Link"):
            c.execute("INSERT INTO characterfaction (character_id, faction_id) VALUES (%s, %s)",
                      (char_dict[char], fac_dict[fac]))
            conn.commit()
            st.success(f"Linked {char} to {fac}")

# --- Close connection ---
conn.close()
st.markdown("---")
st.caption("Loreweave Admin Console")










