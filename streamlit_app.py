import streamlit as st
from datetime import datetime, timedelta
import pytz
import time

# Title for the app
st.title('Delivery Time Calculator')

# Create a state variable to store the completion time (initially None)
if 'completion_time' not in st.session_state:
    st.session_state['completion_time'] = None

# Create a state variable to track whether the timer is running
if 'is_calculating' not in st.session_state:
    st.session_state['is_calculating'] = False

# Create a state variable to store comments (initially an empty list)
if 'comments' not in st.session_state:
    st.session_state['comments'] = []

# Input fields for total delivery navigation time and number of deliveries
if not st.session_state['is_calculating']:
    nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
    num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

    # Calculate total time
    total_time = nav_time + (5 * num_deliveries)

    # Button to calculate delivery completion time
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
        st.session_state['is_calculating'] = True  # Set calculating state to True

# If a completion time exists and is a valid datetime object, display the countdown
if st.session_state['is_calculating']:
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
                    I will be back in {hours:02}:{minutes:02}:{seconds:02} (HH:MM:SS)
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

# Add a reset button at the bottom
if st.button("Reset"):
    # Clear the session state
    st.session_state['completion_time'] = None
    st.session_state['is_calculating'] = False

# Message board
st.subheader("Message Board")

# Text area for new comments
new_comment = st.text_area("Write your comment here:")

# Button to submit the comment
if st.button("Submit Comment"):
    if new_comment:  # Check if the text area is not empty
        st.session_state['comments'].append(new_comment)  # Add comment to the list
        st.success("Comment added!")  # Show a success message
    else:
        st.warning("Please enter a comment before submitting.")  # Warning if empty

# Display existing comments
if st.session_state['comments']:
    st.write("### Existing Comments:")
    for comment in st.session_state['comments']:
        st.write(f"- {comment}")  # Display each comment in a list format
