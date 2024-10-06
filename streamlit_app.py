import streamlit as st
from datetime import datetime, timedelta
import pytz
import time
import os

# File to store messages
MESSAGE_FILE = 'messages.txt'

# Function to read messages from the file
def read_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as f:
            return f.readlines()
    return []

# Function to write a new message to the file
def write_message(msg):
    with open(MESSAGE_FILE, 'a') as f:
        f.write(f"{datetime.now(pytz.utc).isoformat()}: {msg}\n")

# Title for the app
st.title('Delivery Time Calculator and Chat Feature')

# Create a state variable to store the completion time (initially None)
if 'completion_time' not in st.session_state:
    st.session_state['completion_time'] = None

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

# Calculate total time
total_time = nav_time + (5 * num_deliveries)

if st.button('Calculate Delivery Completion Time'):
    current_time_utc = datetime.now(pytz.utc)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)
    st.session_state['completion_time'] = completion_time_kst

# Chat functionality
st.subheader('Chat Room')
message = st.text_input("Type your message:")
if st.button('Send'):
    if message:
        write_message(message)  # Save message to file
        st.experimental_rerun()  # Rerun to update chat display

# Display chat messages
st.subheader('Messages')
messages = read_messages()
if messages:
    for msg in messages:
        st.markdown(f"> {msg.strip()}")

# Countdown functionality
if 'completion_time' in st.session_state:
    countdown_container = st.empty()
    while True:
        current_time = datetime.now(pytz.timezone('Asia/Seoul'))
        time_remaining = st.session_state['completion_time'] - current_time
        if time_remaining.total_seconds() > 0:
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_container.markdown(f"""
                <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                    I will be back in {hours:02}:{minutes:02}:{seconds:02}
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        else:
            countdown_container.markdown(f"""
                <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                    I am back now!
                </div>
            """, unsafe_allow_html=True)
            break
