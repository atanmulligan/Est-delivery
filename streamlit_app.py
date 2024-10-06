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

if st.button('Calculate Delivery Completion Time'):
    current_time_utc = datetime.now(pytz.utc)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)
    st.session_state['completion_time'] = completion_time_kst
    st.success("Completion time calculated!")  # Optional feedback for the user

# Countdown display
countdown_container = st.empty()  # Create a placeholder for countdown

# Function to update countdown
def update_countdown():
    while True:
        current_time = datetime.now(pytz.timezone('Asia/Seoul'))
        if 'completion_time' in st.session_state and st.session_state['completion_time'] is not None:
            time_remaining = st.session_state['completion_time'] - current_time
            
            if time_remaining.total_seconds() > 0:
                minutes, seconds = divmod(time_remaining.seconds, 60)

                # Display the countdown
                countdown_container.markdown(f"""
                    <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                        I will be back in {minutes:02} minutes, {seconds:02} seconds
                    </div>
                """, unsafe_allow_html=True)

                # Display total time remaining in a separate line
                total_time_remaining = timedelta(minutes=nav_time) + timedelta(seconds=(5 * num_deliveries))
                total_minutes, total_seconds = divmod(total_time_remaining.seconds, 60)
                
                countdown_container.markdown(f"""
                    <div style="font-size: 24px; text-align: center; color: #555;">
                        Total Time Remaining: {total_minutes:02} minutes, {total_seconds:02} seconds
                    </div>
                """, unsafe_allow_html=True)
            else:
                countdown_container.markdown(f"""
                    <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                        I am back now!
                    </div>
                """, unsafe_allow_html=True)
                break  # Exit the loop if time is up

            # Get the completion time in KST for display
            completion_time_kst_str = st.session_state['completion_time'].strftime('%Y-%m-%d %H:%M:%S')
            countdown_container.markdown(f"""
                <div style="font-size: 24px; text-align: center; color: #555;">
                    Completion Time (KST): {completion_time_kst_str}
                </div>
            """, unsafe_allow_html=True)

        time.sleep(1)  # Wait for 1 second before the next update

# Start the countdown if a completion time exists
if st.session_state['completion_time'] is not None:
    update_countdown()
