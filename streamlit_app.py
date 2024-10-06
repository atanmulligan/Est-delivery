import streamlit as st
from datetime import datetime, timedelta

# Title for the app
st.title('Delivery Time Calculator')

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

# Formula: total_time = nav_time + (5 * num_deliveries)
if st.button('Calculate Delivery Completion Time'):
    total_time = nav_time + (5 * num_deliveries)
    
    # Get current time
    current_time = datetime.now()

    # Calculate the completion time by adding the total time to the current time
    completion_time = current_time + timedelta(minutes=total_time)
    
    # Display the total time result and the delivery completion time (formatted without seconds or year)
    st.write(f'Total time needed for deliveries: {total_time} minutes')
    st.write(f'Deliveries will be completed by: {completion_time.strftime("%I:%M %p on %B %d")}')
