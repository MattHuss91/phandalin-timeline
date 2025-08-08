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

def get_all(table, id_col, name_col, sort_by_name=True, sort_by_world_day=False):
    if sort_by_world_day:
        c.execute(f"SELECT {id_col}, {name_col} FROM {table} ORDER BY world_day")
    elif sort_by_name:
        c.execute(f"SELECT {id_col}, {name_col} FROM {table} ORDER BY {name_col}")
    else:
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
        c.execute("SELECT name, type, status, bio, is_player, character_img FROM characters WHERE character_id = %s", (cid,))
        row = c.fetchone()
        with st.form("edit_char"):
            name = st.text_input("Name", value=row[0])
            ctype = st.text_input("Type", value=row[1])
            status = st.text_input("Status", value=row[2])
            bio = st.text_area("Bio", value=row[3])
            is_player = st.checkbox("Is Player?", value=row[4])
            character_img = st.text_input("Character Image URL", value=row[5])
            if st.form_submit_button("Update"):
                c.execute("UPDATE characters SET name=%s, type=%s, status=%s, bio=%s, is_player=%s, character_img=%s WHERE character_id = %s",
                          (name, ctype, status, bio, is_player, character_img, cid))
                conn.commit()
                st.success("Character updated.")
    else:
        with st.form("create_char"):
            name = st.text_input("Name")
            ctype = st.text_input("Type")
            status = st.text_input("Status")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            character_img = st.text_input("Character Image Url")
            if st.form_submit_button("Create"):
                c.execute("INSERT INTO characters (name, type, status, bio, is_player, character_img) VALUES (%s, %s, %s, %s, %s, %s)",
                          (name, ctype, status, bio, is_player, character_img))
                conn.commit()
                st.success("Character created.")

# --- Events ---
elif mode == "Events":
    submode = st.radio("Action", ["Create", "Edit"])
    if submode == "Edit":
        events = get_all("campaignevents", "event_id", "title", sort_by_name=False, sort_by_world_day=True)
        event_dict = {name: eid for eid, name in events}

        locs = get_all("locations", "location_id", "name")
        locs_sorted = sorted(locs, key=lambda x: x[0])
        loc_names = [name for _, name in locs_sorted]
        loc_id_by_name = {name: lid for lid, name in locs_sorted}

        selected = st.selectbox("Select Event", list(event_dict.keys()))
        eid = event_dict[selected]

        c.execute("""
            SELECT e.title,
                   e.date_occurred,
                   e.location_id,
                   l.name AS location_name,
                   e.summary,
                   e.full_description
            FROM campaignevents e
            LEFT JOIN locations l ON e.location_id = l.location_id
            WHERE e.event_id = %s
        """, (eid,))
        row = c.fetchone()

        with st.form("edit_event"):
            title = st.text_input("Title", value=row[0])
            date_occurred = st.text_input("Date Occurred", value=row[1])

            current_loc_id = row[2]
            try:
                current_index = next(i for i, (lid, _) in enumerate(locs_sorted) if lid == current_loc_id)
            except StopIteration:
                current_index = 0
            loc_name = st.selectbox("Location", loc_names, index=current_index)

            summary = st.text_area("Summary", value=row[4])
            full_description = st.text_area("Full Description", value=row[5])

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
                    loc_id_by_name[loc_name],
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
    else:
        locs = get_all("locations", "location_id", "name")
        locs_sorted = sorted(locs, key=lambda x: x[0])
        loc_names = [name for _, name in locs_sorted]
        loc_id_by_name = {name: lid for lid, name in locs_sorted}

        with st.form("create_event"):
            title = st.text_input("Title")
            date_occurred = st.text_input("Date Occurred (e.g., 4th Verdanir 1041)")
            loc_name = st.selectbox("Location", loc_names)
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
                        loc_id_by_name[loc_name],
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

    if submode == "Create":
        with st.form("create_loc"):
            name = st.text_input("Name")
            reg = st.text_input("Region")
            desc = st.text_area("Description")
            if st.form_submit_button("Create"):
                c.execute("INSERT INTO locations (name, region, description) VALUES (%s, %s, %s)", (name, reg, desc))
                conn.commit()
                st.success("Location created.")

    else:
        locs = get_all("locations", "location_id", "name")
        loc_dict = {name: lid for lid, name in locs}
        selected = st.selectbox("Select Location", [name for _, name in locs])
        lid = loc_dict[selected]

        c.execute("SELECT name, region, description FROM locations WHERE location_id = %s", (lid,))
        row = c.fetchone()

        with st.form("edit_loc"):
            name = st.text_input("Name", value=row[0])
            region = st.text_input("Region", value=row[1])
            description = st.text_area("Description", value=row[2])

            if st.form_submit_button("Update"):
                c.execute("""
                    UPDATE locations
                    SET name = %s, region = %s, description = %s
                    WHERE location_id = %s
                """, (name, region, description, lid))
                conn.commit()
                st.success("Location updated.")

# --- Factions ---
elif mode == "Factions":
    submode = st.radio("Action", ["Create", "Edit"])

    if submode == "Edit":
        factions = get_all("factions", "faction_id", "name")

        fac_dict = {name: fid for fid, name in factions}

        selected = st.selectbox("Select Faction", list(fac_dict.keys()))
        fid = fac_dict[selected]

        c.execute(
            "SELECT name, alignment, goals, faction_img FROM factions WHERE faction_id = %s",
            (fid,)
        )
        row = c.fetchone()

        with st.form("edit_faction"):
            name = st.text_input("Name", value=row[0] or "")
            ali = st.text_input("Alignment", value=row[1] or "")
            desc = st.text_area("Description", value=row[2] or "")
            faction_img = st.text_input("Faction Image URL", value=row[3] or "")
            if st.form_submit_button("Update"):
                c.execute(
                    "UPDATE factions SET name = %s, alignment = %s, goals = %s, faction_img = %s WHERE faction_id = %s",
                    (name, ali, desc, faction_img, fid)
                )
                conn.commit()
                st.success("Faction updated.")

    else:
        with st.form("create_faction"):
            name = st.text_input("Name")
            ali = st.text_input("Alignment")
            desc = st.text_area("Description")
            faction_img = st.text_input("Faction Image URL")
            if st.form_submit_button("Create"):
                c.execute(
                    "INSERT INTO factions (name, alignment, goals, faction_img) VALUES (%s, %s, %s, %s)",
                    (name, ali, desc, faction_img)
                )
                conn.commit()
                st.success("Faction created.")


# --- Link Character to Event ---
elif mode == "Link Character to Event":
    chars = get_all("characters", "character_id", "name")
    events = get_all("campaignevents", "event_id", "title", sort_by_name=False, sort_by_world_day=True)
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







