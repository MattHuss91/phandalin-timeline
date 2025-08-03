import streamlit as st

st.set_page_config(
    page_title="Home",     # <- Sidebar shows "Home"
    page_icon="📜",        # <- Optional: gives a nice emoji icon
    layout="centered"
)
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

    .stContainer {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)


st.title("The Heroes of Phandalin")
st.write("The box was just the start")

# User list
usernames = ["Admin", "Emily", "Kay", "Jon", "Chris", "Hans"]

# If not logged in, show login form
if "username" not in st.session_state or st.session_state["username"] is None:
    selected_user = st.selectbox("Select your user", usernames)
    if st.button("Log in"):
        st.session_state.username = selected_user
        st.experimental_rerun()
else:
    st.success(f"Logged in as {st.session_state['username']}")
    if st.button("Log out"):
        del st.session_state["username"]
        st.experimental_rerun()
