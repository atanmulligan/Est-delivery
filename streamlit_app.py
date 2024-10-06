import streamlit as st
from datetime import datetime, timedelta
import pytz

# Title for the app
st.title('Delivery Time Calculator')

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

# Formula: total_time = nav_time + (5 * num_deliveries)
if st.button('Calculate Delivery Completion Time'):
    total_time = nav_time + (5 * num_deliveries)
    
    # Get current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert current time to Korea Standard Time (KST)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)

    # Calculate the completion time by adding the total time to the current time in KST
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)
    
    # Display the total time result and the delivery completion time (formatted without seconds or year)
    st.write(f'Total time needed for deliveries: {total_time} minutes')
    st.write(f'Deliveries will be completed by: {completion_time_kst.strftime("%I:%M %p on %B %d")} KST')
