import streamlit as st

# Title for the app
st.title('Delivery Time Calculator')

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('Enter total delivery navigation time (in minutes):', min_value=0)
num_deliveries = st.number_input('Enter number of deliveries:', min_value=0)

# Formula: total_time = nav_time + (5 * num_deliveries)
if st.button('Calculate Total Time'):
    total_time = nav_time + (5 * num_deliveries)
    
    # Display the total time result
    st.write(f'Total time needed for deliveries: {total_time} minutes')

import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
