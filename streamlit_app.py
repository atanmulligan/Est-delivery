import streamlit as st
from datetime import datetime, timedelta
import pytz

# Title for the app
st.title('Delivery Time Calculator')

# Default admin password (for demonstration purposes, you may want to store this securely)
ADMIN_PASSWORD = "admin"

# Create a state variable to store time adjustment (initially 0)
if 'time_adjustment' not in st.session_state:
    st.session_state['time_adjustment'] = 0

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

# Section for admin to adjust the total time
st.subheader("Admin Time Adjustment")
admin_password = st.text_input("Enter admin password to adjust time:", type="password")

if admin_password == ADMIN_PASSWORD:
    adjustment = st.number_input('Enter number of extra or less minutes for deliveries (positive for extra, negative for less):', min_value=-60, max_value=60)
    if st.button("Update Time Adjustment"):
        st.session_state['time_adjustment'] = adjustment
        st.success(f"Time adjusted by {adjustment} minutes.")
else:
    st.info("Please enter the correct admin password to adjust the time.")

# Calculate total time including the adjustment
total_time = nav_time + (5 * num_deliveries) + st.session_state['time_adjustment']

# Formula: total_time = nav_time + (5 * num_deliveries) + adjustment
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
    st.write(f'Total time needed for deliveries (including adjustments): {total_time} minutes')

# If a completion time exists, it will automatically be displayed at the top as well
