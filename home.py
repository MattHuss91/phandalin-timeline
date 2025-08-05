import streamlit as st
import os

# Custom Fantasy Styling
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

    /* Button container */
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

st.image("https://i.imgur.com/WEGvkz8.png", use_container_width=True)
st.title("Loreweave")
st.write("Heroes of Phandalin")

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

