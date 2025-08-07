import streamlit as st
import os

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

#date config

from datetime import date

def get_current_fantasy_date():
    # --- Config ---
    fantasy_months = [
        "Verdanir", "Emberfall", "Duskwatch", "Glimmerwane", "Brightreach",
        "Stormrest", "Hollowshade", "Deepmoor", "Frostmere", "Starwake"
    ]
    weekdays = ["Sunsday", "Moonday", "Wyrmday", "Gloomday", "Thornsday", "Brightsday"]
    days_per_month = 36
    days_per_year = 360

    # --- Date Calculations ---
    anchor = date(2025, 1, 1)  # Real-world Day 1
    today = date.today()
    days_since_anchor = (today - anchor).days
    world_day_number = days_since_anchor % days_per_year

    # --- Fantasy Date ---
    month_index = world_day_number // days_per_month
    day_of_month = (world_day_number % days_per_month) + 1
    weekday = weekdays[days_since_anchor % 6]

    # --- Return as dict ---
    return {
        "weekday": weekday,
        "day": day_of_month,
        "month": fantasy_months[month_index],
        "irl": today.strftime("%A %d %B")
    }

# logo
st.markdown("""
    <div style='text-align: center; margin-top: -20px;'>
        <img src='https://i.imgur.com/WEGvkz8.png' style='width: 200px; margin-bottom: -10px;' />
        <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>Heroes of Phandalin</h1>
    </div>
""", unsafe_allow_html=True)

# --- Get fantasy date ---
fantasy_date = get_current_fantasy_date()

# --- Display it ---
st.markdown(f"""
<div style='
    background-color: rgba(255, 255, 255, 0.8);
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-family: "Lora", serif;
    text-align: center;
    margin-bottom: 1rem;
'>
    📅 <strong>Today in the world:</strong><br>
    <em>{fantasy_date['weekday']}, {fantasy_date['day']} {fantasy_date['month']}</em><br>
    <small>(IRL: {fantasy_date['irl']})</small>
</div>
""", unsafe_allow_html=True)

# User list
usernames = ["Admin", "Emily", "Kay", "Jon", "Chris", "Hans"]

# Username: Password pairs
users = {
    "Admin": "adminpass",
    "Emily": "ceridwen",
    "Kay": "fariah",
    "Jon": "llechan",
    "Chris": "geoff",
    "Hans": "sister"
}

# If not logged in, show login form
if "username" not in st.session_state or st.session_state["username"] is None:
    selected_user = st.selectbox("Select your user", list(users.keys()))
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        if users[selected_user] == password:
            st.session_state.username = selected_user

            
            if selected_user == "Admin":
                st.session_state.user_role = "Admin"
            else:
                st.session_state.user_role = "Player"

            st.rerun()
        else:
            st.error("Incorrect password")

else:
    st.success(f"Logged in as {st.session_state['username']}")
    if st.button("Log out"):
        del st.session_state["username"]
        del st.session_state["user_role"]
        st.rerun()

st.markdown("---")
st.caption("Loreweave")

