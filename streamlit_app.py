import streamlit as st
from datetime import datetime, timedelta
import pytz

# Title for the app
st.title('Delivery Time Calculator')

# Create a state variable to store the completion time (initially None)
if 'completion_time' not in st.session_state:
    st.session_state['completion_time'] = None

# If a completion time exists, display it at the top
if st.session_state['completion_time']:
    st.markdown(f"""
        <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
            Deliveries will be completed by: {st.session_state['completion_time']} KST
        </div>
    """, unsafe_allow_html=True)

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

    # Format the completion time and store it in the session state
    completion_time_formatted = completion_time_kst.strftime("%I:%M %p on %B %d")
    st.session_state['completion_time'] = completion_time_formatted

    # Display the total time result
    st.write(f'Total time needed for deliveries: {total_time} minutes')

# If a completion time exists, it will automatically be displayed at the top as well
