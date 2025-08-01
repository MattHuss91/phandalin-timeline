character_bio_lookup = {'Llechan': "lechan's tribe of Tabaxi lived and worked in a quarrying community. One day, an ancient relic with magical essence was found whilst carving out a new cavern. The village wise men began to examine this, but accidentally unlocked dark magic that had been sealed within. This lead to the land being frozen overnight. Those who didn't die in these sudden conditions struggled to adapt to this new life. All those who had studied the relic were killed, and the relic itself was lost. From this, the rangers were born, a group of skilled survivalists who were sent out to try and find a way of reversing the curse. As far as he knows, Llechan is the last survivor of this group. He has become aware that the Dwarven Lords may have information concerning the type of magic used to freeze his land, therefore he has assigned himself to support the dwarves in any way he can, hoping that one day his deeds will earn him an audience with the lords, at which point he can make a request for information.", 'Ceridwen': '2 children, Creirwy (daughter) and Morfran (son). Creirwy is beautiful but Morfran is hideously ugly. ', 'Barry': 'Barry is not sure where he came from, or why he is here. He is inflicted wih a rare form of elephathorpy allowing him to turn into an elephant man. He is in search for belonging', "Fa'riah": "Fa'riah began life as the child of two Witchlight Carnival hands who lived a carefree life travelling with the Carnival between planes. ", 'Sister': 'Sister was banished from her tribe so long ago that she cannot remember what she has done. She found her way to a monastery of Lathander and dedicated her life to going good in his light. She has been there for over 100 years and has now forgotten her original name and goes by the title Sister. ', 'Geoff': "Geoff has inherited his father's restaurant chain called the golden potato after he was killed by the spiders goons when they were trying to get their protection money from him. Geoff is looking for revenge against the spider who he holds accountable. ", 'Sildar Hallwinter': "Trusted friend of the Rockseeker family and leading member of the Lord's Alliance. Don't let his age fool you. Sildar is a skilled paladin and is the most loyal man you will meet in all the realms", 'Klarg': 'The brutal and commanding leader of the Cragmar Clan. Known for his cruelty and his love of wolves', 'Gundren Rockseeker': 'A hill dwarf with a heart of gold. Him and his brother Wugren found the location of the speel forge, since then life has been a bit of a rollercoaster', 'Droop': 'If hope was personified it would be Droop. Born a weak goblin and frequently bullied by his peers. His life was turned around when he met the heroes of phandalin. Does to being the only living goblin from the Cragmar clan, Droop is now considered the King of Goblins. Which is a big step up from his humble start.', 'Nilsa Dendar': 'Born shortly before the fall of Thundertree, she remembers little of her home town. Having discovered the puzzle box and accidently opening it, she was given wild magical powers. She is slowly learnign to control them, and has prooved to be a valuable ally to the Heroes. ', 'Pip Dendar': 'A small boy born after the fall of Thundertree. Fuill of hope and child like wonder.', 'Mirna Dendar': 'Protective over her children and greiving the death of her husband. Mirna is the matriarch of the Dendar family. ', 'Illarno ': 'Once a close friend of Sildar and a member of the Lords Alliance, Illarno fell under the influence of The Spider and became the leader of the Redbrands. He was a powerful wizard and a cunning manipulator.  ', 'The Black Spider': 'The Black Spider is a shape-shifting changeling and master manipulator. Raised in a cruel drow orphanage, he was tormented by others until a series of mysterious murders (later revealed to be his own hidden actions) set him on a path of darkness. Discovering his true nature, he became obsessed with an ancient puzzle box said to contain the heart of a god. Through deception, seduction, and sorcery, he tricked others into unlocking it, causing devastation across the realm. Cold, calculating, and haunted by fragmented identities, the Black Spider walks the line between tragic victim and apocalyptic threat.', 'Taliesin': 'Taliesin is a mysterious and powerful figure tied deeply to Ceridwen’s past. Born from forbidden magic and raised in the shadows of secrets, he has become both a legend and a threat. Once a hopeful soul, his path diverged after learning of his origins; blending pain, purpose, and prophecy. Charismatic and cunning, Taliesin operates from the edges of conflict, manipulating events in pursuit of a fate only he seems to understand. Whether ally, enemy, or something in between, Taliesin remains a figure of unfinished business and untold consequences.', 'Aletha': 'A half Elf Rouge. She was determined to find a family relic in the town of Thundertree. Eventually her goal became her undoing. She was killed by the cultists of Venomfang', 'Venomfang': 'Venomfang is an ancient green dragon who once ruled the ruins of Thundertree with cruel amusement. Arrogant, sadistic, and supremely intelligent, he delights in psychological torment as much as physical domination. When the party encountered him, he toyed with them; offering a false head start so he could hunt them for sport. Though they ultimately escaped and later returned to face him, Venomfang’s presence left a scar of fear and fury. He is the embodiment of predatory pride: a force of nature that treats adventurers as entertainment, not threat.', 'Kadia': 'A trapped soul of a tabaxi. She could not pass to the otherside until the cursed diary was handed over to another. She was eventually able to pass when the party opened the diary and learnt the history of the spider', 'Icy Fire': 'Once a normal Tabaxi. He was manipulated by the Spider to open the puzzle box and plunge the land of Fandora into a desolate wasteland. He was corrupted by an being know oas "The Entity of Rage". He nearly killed the party before they were saved by Eilistraee', 'Eilistraee': 'Eilistraee is the drow goddess of moonlight, beauty, song, swordplay, and redemption. She is one of the few deities to offer compassion and hope to the drow, guiding those who wish to escape Lolth’s darkness and find a life of peace on the surface. Often appearing as a dancing, silver-haired woman under moonlight, Eilistraee teaches that joy, freedom, and kindness are sacred. Her followers often help lost souls, protect the innocent, and use music and dance as acts of divine expression. Though gentle, she is not weak — and when evil must be faced, her blade sings.', 'The Entiy of Rage': 'A being of pure range. one of multiple Entitiies the party have met on their travels', 'Corvin Blackthorn': 'A mysterious Human warlock bound to a forgotten power, Corvin walks the line between shadow and salvation. Taciturn but fiercely loyal, he joined the party after a shared vision revealed a greater threat lurking beyond the material plane. Though his past remains veiled, his magic speaks of ancient pacts and unhealed scars.', 'The Entity of Loss': 'A being formed by the feelign of loos. It forces all of the hope and goodness out of a person and feeds on their memories. The party were able to best the Entity, but its fate remains unknown'}


import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Timeline", layout="centered")

# Custom Fantasy Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lora', serif !important;
        color: #000000 !important;
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }

    .stContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Phandalin Campaign Timeline")

# Connect to database
conn = sqlite3.connect("dnd_campaign.db")
cursor = conn.cursor()

# Ensure the EventTimeline view exists
cursor.executescript("""
DROP VIEW IF EXISTS EventTimeline;

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
    GROUP_CONCAT(c.name, ', ') AS people_involved
FROM CampaignEvents ce
LEFT JOIN characterappearances ca ON ce.event_id = ca.event_id
LEFT JOIN characters c ON ca.character_id = c.character_id
LEFT JOIN Locations l ON ce.location_id = l.location_id
GROUP BY ce.event_id;
""")

# Load events from view
events_df = pd.read_sql_query("SELECT * FROM EventTimeline ORDER BY world_day", conn)

# Character filter
all_characters = events_df['people_involved'].str.split(', ').explode().dropna().unique()
selected_character = st.selectbox("Filter by character", ["All"] + sorted(all_characters.tolist()))

if selected_character != "All":
    events_df = events_df[events_df['people_involved'].str.contains(selected_character)]

# Get slider range from filtered data
labels = events_df['date_occurred'].tolist()
day_to_label = dict(zip(events_df['world_day'], events_df['date_occurred']))
label_to_day = {v: k for k, v in day_to_label.items()}

selected_start, selected_end = st.select_slider(
    "Select a date range",
    options=labels,
    value=(labels[0], labels[-1])
)

start_day = label_to_day[selected_start]
end_day = label_to_day[selected_end]

# Filter by selected date range
filtered_events = events_df[(events_df['world_day'] >= start_day) & (events_df['world_day'] <= end_day)]

# Display the events
for _, row in filtered_events.iterrows():
    st.header(row['title'])
    st.write(f"{row['date_occurred']} — {row['location']}")
    
    st.markdown("**People Involved:**")
    for character in row['people_involved'].split(', '):
        if character in character_bio_lookup:
            with st.expander(character):
                st.write(character_bio_lookup[character])
        else:
            st.write(character)
    

    with st.expander(f"Summary: {row['summary']}"):
        st.write(row['full_description'])

conn.close()
