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

st.title("The Heroes of Phandalin")
st.write("The box was just the start")
