import streamlit as st
import psycopg2
import pandas as pd
import urllib.parse

# --- Streamlit config ---
st.set_page_config(page_title="locations", layout="centered")
user = st.session_state.get("username")

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

    label {
        color: #000000 !important;
        font-weight: bold;
    }

    div.stButton > button {
        background-color: #333333 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
    <div style='text-align: center; margin-top: -20px;'>
        <img src='https://i.imgur.com/WEGvkz8.png' style='width: 200px; margin-bottom: -10px;' />
        <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>locations</h1>
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

# --- Load location data ---
location_df = pd.read_sql_query("SELECT location_id, name, region, description FROM locations ORDER BY name", conn)#

# --- location dropdown ---
location_name = sorted(location_df["name"].tolist())
selected_location = st.selectbox("Choose a Location", location_name)
location_row = location_df[location_df["name"] == selected_location].iloc[0]
location_id = int(location_row["location_id"])

# --- Display Location Info ---
st.header(selected_location)

if location_row["region"]:
    st.subheader(f"Region: {location_row['region']}")

st.write("### Description")
st.write(location_row["description"])


st.markdown("---")
st.caption("Loreweave")








