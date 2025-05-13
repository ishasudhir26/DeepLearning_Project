import streamlit as st
import base64

# Set page configuration
st.set_page_config(page_title='Hand Gesture - Based Media Control System', layout='wide')

# Hide Streamlit style elements (top pane and footer)
hide_st_style = '''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to set background image
def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()
    bg_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

# Set the background image
set_bg("background.jpeg")

# Center the title
st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; height: 60vh; padding: 0 20px; text-align: center;'>
        <h1 style='font-size: 3.5rem; font-weight: bold; color: #FFFFFF;'>HAND GESTURE - BASED MEDIA CONTROL SYSTEM</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Goal and Applications
st.sidebar.title("About")
st.sidebar.markdown("""
This system provides a hands-free control mechanism for media players using hand gesture recognition, enhancing accessibility and user convenience.
It gives hands-free control of media players.

Navigate through the other page for instructions and to control the media.
""")
