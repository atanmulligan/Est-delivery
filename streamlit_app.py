import streamlit as st
from datetime import datetime, timedelta
import pytz
import os
import time

# File to store messages
MESSAGE_FILE = 'messages.txt'
ADMIN_PASSWORD = 'admin'  # Predefined admin password

# Function to read messages from the file
def read_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as f:
            return f.readlines()
    return []

# Function to write a new message to the file
def write_message(msg):
    with open(MESSAGE_FILE, 'a') as f:
        f.write(f"{msg}\n")  # Write only the message content

# Function to reset messages
def reset_messages():
    if os.path.exists(MESSAGE_FILE):
        os.remove(MESSAGE_FILE)

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
    st.success("Completion time calculated!")  # Optional feedback for the user

# Chat functionality
st.subheader('Chat Room')

# Check for the message input and button press
message = st.text_input("Type your message:")
if st.button('Send'):
    if message:
        write_message(message)  # Save message to file
        st.success("Message sent!")  # Optional feedback for the user

# Placeholder for messages
message_placeholder = st.empty()

# Function to display messages
def display_messages():
    messages = read_messages()
    message_placeholder.markdown("### Messages")
    if messages:
        for msg in messages:
            message_placeholder.markdown(f"> {msg.strip()}")  # Show only the message content
    else:
        message_placeholder.markdown("No messages yet.")

# Countdown functionality
if 'completion_time' in st.session_state and st.session_state['completion_time'] is not None:
    countdown_container = st.empty()
    
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
    else:
        countdown_container.markdown(f"""
            <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                I am back now!
            </div>
        """, unsafe_allow_html=True)

# Admin functionality to reset messages
st.subheader('Admin Control')

admin_password = st.text_input("Enter admin password to reset messages:", type='password')

if st.button('Reset Messages'):
    if admin_password == ADMIN_PASSWORD:
        reset_messages()
        st.success("Messages have been reset!")
    else:
        st.error("Incorrect password. Access denied.")

# Automatically refresh messages every 5 seconds
if st.button('Start Message Refresh'):
    st.session_state.refreshing = True  # Start refreshing
    st.session_state.last_update = time.time()  # Record the last update time

# Stop refreshing messages
if st.button('Stop Message Refresh'):
    st.session_state.refreshing = False

# Check and refresh messages
if 'refreshing' in st.session_state and st.session_state.refreshing:
    while True:
        current_time = time.time()
        
        if current_time - st.session_state.last_update >= 5:  # Check every 5 seconds
            display_messages()  # Display the latest messages
            st.session_state.last_update = current_time  # Update the last update time

        time.sleep(1)  # Avoid tight loops
