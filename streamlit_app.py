import streamlit as st
from datetime import datetime, timedelta
import pytz
import time

# Title for the app
st.title('Delivery Time Calculator')

# Create a state variable to store the completion time (initially None)
if 'completion_time' not in st.session_state:
    st.session_state['completion_time'] = None

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

# Calculate total time
total_time = nav_time + (5 * num_deliveries)

# Formula: total_time = nav_time + (5 * num_deliveries)
if st.button('Calculate Delivery Completion Time'):
    # Get current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert current time to Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)

    # Calculate the completion time by adding the total time to the current time in KST
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)

    # Store the completion time in session state as a datetime object
    st.session_state['completion_time'] = completion_time_kst

# If a completion time exists and is a valid datetime object, display the countdown
if isinstance(st.session_state['completion_time'], datetime):
    countdown_container = st.empty()

    while True:
        # Get the current time
        current_time = datetime.now(pytz.timezone('Asia/Seoul'))

        # Calculate the difference between completion time and current time
        time_remaining = st.session_state['completion_time'] - current_time

        if time_remaining.total_seconds() > 0:
            # Extract hours, minutes, and seconds from the remaining time
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Display the countdown in the desired format
            countdown_container.markdown(f"""
                <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                    I will be back in {hours:02}:{minutes:02}:{seconds:02}
                </div>
            """, unsafe_allow_html=True)

            # Sleep for 1 second before updating the countdown
            time.sleep(1)
        else:
            countdown_container.markdown(f"""
                <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                    I am back now!
                </div>
            """, unsafe_allow_html=True)
            break
