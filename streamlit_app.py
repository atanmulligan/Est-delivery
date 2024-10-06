import streamlit as st
from datetime import datetime, timedelta
import pytz

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

if st.button('Calculate Delivery Completion Time'):
    current_time_utc = datetime.now(pytz.utc)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)
    st.session_state['completion_time'] = completion_time_kst
    st.success("Completion time calculated!")  # Optional feedback for the user

# Countdown display
countdown_container = st.empty()  # Create a placeholder for countdown

if 'completion_time' in st.session_state and st.session_state['completion_time'] is not None:
    current_time = datetime.now(pytz.timezone('Asia/Seoul'))
    time_remaining = st.session_state['completion_time'] - current_time

    if time_remaining.total_seconds() > 0:
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Calculate the KST completion time
        completion_time_kst_str = st.session_state['completion_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        # Display the countdown and the completion time
        countdown_container.markdown(f"""
            <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                I will be back in {hours:02}:{minutes:02}:{seconds:02} (Completion Time: {completion_time_kst_str} KST)
            </div>
        """, unsafe_allow_html=True)
    else:
        countdown_container.markdown(f"""
            <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                I am back now!
            </div>
        """, unsafe_allow_html=True)
