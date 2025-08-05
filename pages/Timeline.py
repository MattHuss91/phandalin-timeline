import streamlit as st
import psycopg2
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Timeline", layout="centered")

# Read query parameters
query_params = st.query_params
highlight_event = query_params.get("highlight", [""])[0]
from_character_id = query_params.get("from_character_id", [""])[0]

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
    </style>
""", unsafe_allow_html=True)

st.title("Phandalin Campaign Timeline")

# Connect to Supabase PostgreSQL
conn = psycopg2.connect(
    host=st.secrets["db_host"],
    dbname=st.secrets["db_name"],
    user=st.secrets["db_user"],
    password=st.secrets["db_password"],
    port=st.secrets["port"],
    sslmode="require"
)
c = conn.cursor()

# Create or refresh the EventTimeline view
c.execute("DROP VIEW IF EXISTS EventTimeline CASCADE;")
c.execute("""
    CREATE VIEW EventTimeline AS
    SELECT 
        ce.event_id,
        ce.title,
        ce.date_occurred,
        ce.summary,
        ce.full_description,
        ce.day,
        ce.month,
        ce.year,
        ce.world_day,
        l.name AS location,
        STRING_AGG(c.name, ', ') AS people_involved
    FROM CampaignEvents ce
    LEFT JOIN characterappearances ca ON ce.event_id = ca.event_id
    LEFT JOIN characters c ON ca.character_id = c.character_id
    LEFT JOIN Locations l ON ce.location_id = l.location_id
    GROUP BY ce.event_id, l.name;
""")
conn.commit()

# Load events
events_df = pd.read_sql_query("SELECT * FROM EventTimeline ORDER BY world_day", conn)

# Highlighted event filter
if highlight_event:
    filtered_df = events_df[events_df["title"].str.strip().str.lower() == highlight_event.strip().lower()]
    if filtered_df.empty:
        st.warning(f"No event found matching: '{highlight_event}'")
    else:
        events_df = filtered_df

# Back to character link
if from_character_id.isdigit():
    character_id = int(from_character_id)
    c.execute("SELECT name FROM characters WHERE character_id = %s", (character_id,))
    result = c.fetchone()
    if result:
        character_name = result[0]
        encoded_name = urllib.parse.quote(character_name)
        st.markdown(f"[← Back to {character_name}](/character_profiles?character_id={character_id})")

# Filters (if not highlighting a specific event)
if not highlight_event:
    all_characters = events_df['people_involved'].str.split(', ').explode().dropna().unique()
    selected_character = st.selectbox("Filter by character", ["All"] + sorted(all_characters.tolist()))

    if selected_character != "All":
        events_df = events_df[events_df['people_involved'].str.contains(selected_character)]

    # Clean date range slider (with world_day)
date_options = events_df[['world_day', 'date_occurred']].drop_duplicates().sort_values('world_day')

if not date_options.empty:
    day_to_label = dict(zip(date_options['world_day'], date_options['date_occurred']))

    start_day, end_day = st.select_slider(
        "Select a date range",
        options=date_options['world_day'].tolist(),
        format_func=lambda x: day_to_label[x],
        value=(date_options['world_day'].iloc[0], date_options['world_day'].iloc[-1])
    )

    events_df = events_df[
        (events_df['world_day'] >= start_day) & (events_df['world_day'] <= end_day)
    ]
else:
    st.warning("No events found to generate a timeline.")

# Filter dataframe by selected range
events_df = events_df[
    (events_df['world_day'] >= start_day) & (events_df['world_day'] <= end_day)
]

# Render timeline
for _, row in events_df.iterrows():
    st.header(row['title'])
    st.write(f"{row['date_occurred']} — {row['location']}")
    st.markdown(f"**Summary:** {row['summary']}")
    st.write(row['full_description'])

    st.markdown("**People Involved:**")
    for character in row['people_involved'].split(', '):
        c.execute("SELECT character_id FROM characters WHERE name = %s", (character,))
        character_id_query = c.fetchone()
        if character_id_query:
            character_id_link = character_id_query[0]
            st.markdown(f"- [{character}](/character_profiles?character_id={character_id_link})")

conn.close()

st.markdown("---")
st.caption("Loreweave")


