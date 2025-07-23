import streamlit as st

st.set_page_config(
    page_title="Home",     # <- Sidebar shows "Home"
    page_icon="📜",        # <- Optional: gives a nice emoji icon
    layout="centered"
)
# Custom Fantasy Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Uncial+Antiqua&display=swap');

        html, body, .stApp {
            background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
            background-size: cover;
            background-repeat: repeat;
            background-attachment: fixed;
            font-family: 'Uncial Antiqua', serif !important;
            color: #000000;
        }

        * {
            font-family: 'Uncial Antiqua', serif !important;
            color: #000000 !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
        }

        .st-expander {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("The Heroes of Phandalin")
st.write("The box was just the start")
