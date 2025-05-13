import streamlit as st
import base64
import os
import cv2
import numpy as np
import time
import pyautogui
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from tensorflow.keras import backend as K

# Prevent mouseinfo from being imported
pyautogui.mouseInfo = lambda: None

# Set page configuration
st.set_page_config(page_title='Gesture Control', layout='wide')

# Hide Streamlit style elements
hide_st_style = '''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stButton button {
            background-color: #309aa5;
            color: white;
            padding: 12px 24px;
            font-size: 1rem;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-left: 23%
        }
        .stButton button:hover {
            background-color: #267d8a;
            color: black;
        }
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

# Load the model once using st.cache_resource
@st.cache_resource
def load_gesture_model():
    model_path = "best_model_mobilenet2.h5"
    model = load_model(model_path)
    return model

model = load_gesture_model()

# Define the class labels
class_labels = ['Palm', 'Fist', 'Thumbs Up', 'Thumbs Down', 'Index Left', 'Index Right', 'No Gesture']

# Function to predict the gesture
def predict_gesture(frame):
    img = cv2.resize(frame, (120, 120))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])
    predicted_label = class_labels[predicted_class]
    confidence = predictions[0][predicted_class]
    return predicted_label, confidence

# Control media based on the predicted gesture
last_palm_time = 0
palm_cooldown = 0.5

def control_media(label):
    global last_palm_time
    if label == "Palm":
        current_time = time.time()
        if current_time - last_palm_time > palm_cooldown:
            pyautogui.press('space')
            last_palm_time = current_time
    elif label == "Fist":
        pyautogui.press('m')
    elif label == "Thumbs Up":
        pyautogui.press('volumeup')
    elif label == "Thumbs Down":
        pyautogui.press('volumedown')
    elif label == "Index Left":
        pyautogui.press('left')
    elif label == "Index Right":
        pyautogui.press('right')
    elif label == "No Gesture":
        pass

# Instructions Page
st.markdown("""
    <h1 style='color: #309aa5;'>Hand Gesture Instructions</h1>
""", unsafe_allow_html=True)

st.write("""
    <p style='color: #309aa5;'>Below are the hand gestures and their respective functions:</p>
""", unsafe_allow_html=True)

# Sample gesture data
gestures = {
    "Palm": "Play/Pause",
    "Fist": "Mute",
    "Thumbs Up": "Increase Volume",
    "Thumbs Down": "Decrease Volume",
    "Index Left": "Rewind",
    "Index Right": "Forward"
}

# Display gesture instructions in two columns
col1, col2 = st.columns(2)

for idx, (gesture, action) in enumerate(gestures.items()):
    image_path = os.path.join("images", f"{gesture.lower().replace(' ', '_')}.jpg")
    content = f"<p style='color: white; font-size: 1rem;'>{gesture}: {action}</p>"
    if os.path.exists(image_path):
        if idx % 2 == 0:
            with col1:
                st.image(image_path, width=100)
                st.markdown(content, unsafe_allow_html=True)
        else:
            with col2:
                st.image(image_path, width=100)
                st.markdown(content, unsafe_allow_html=True)

# Initialize session state for webcam control
if 'webcam_running' not in st.session_state:
    st.session_state.webcam_running = False

# Webcam control buttons
start_webcam = st.button("Start Webcam")
stop_webcam = st.button("Stop Webcam")
video_placeholder = st.empty()  # Placeholder for the video feed

if start_webcam:
    st.session_state.webcam_running = True
elif stop_webcam:
    st.session_state.webcam_running = False

# Webcam loop controlled by session state
if st.session_state.webcam_running:
    cap = cv2.VideoCapture(0)

    while st.session_state.webcam_running:  # Use session state to control the loop
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 100:400]

        label, confidence = predict_gesture(roi)
        print(f"Gesture: {label}, Confidence: {confidence}")

        frame_with_overlay = frame.copy()
        cv2.rectangle(frame_with_overlay, (100, 100), (400, 400), (0, 255, 0), 2)
        cv2.putText(frame_with_overlay, f"{label} ({confidence:.2f})", (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        video_placeholder.image(frame_with_overlay, channels="BGR")

        control_media(label)

        # Check for the stop button within the loop.
        if stop_webcam:  # This checks the button state.
            st.session_state.webcam_running = False # Stop the loop
            break

    cap.release()
    video_placeholder.empty()

