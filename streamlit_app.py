import streamlit as st
from datetime import datetime, timedelta
import pytz
import time

# Set the title for the browser tab
st.set_page_config(page_title='배달 예상시간 계산기')

# Title for the app
st.title('라이더 배달 예상시간 계산기')

# Create a state variable to store the completion time (initially None)
if 'completion_time' not in st.session_state:
    st.session_state['completion_time'] = None

# Create a state variable to store admin access (initially False)
if 'admin_access' not in st.session_state:
    st.session_state['admin_access'] = False

# Admin password (you can change this to your desired password)
ADMIN_PASSWORD = 'admin123'

# Function to check password
def check_password():
    password = st.text_input("비밀번호 입력:", type='password')
    if st.button('비밀번호 확인'):
        if password == ADMIN_PASSWORD:
            st.session_state['admin_access'] = True
            st.success("비밀번호가 확인되었습니다. 입력 필드를 수정할 수 있습니다.")
        else:
            st.error("잘못된 비밀번호!")

# Input fields for total delivery navigation time and number of deliveries
nav_time = st.number_input('네비시간입력 (in minutes):', min_value=0, disabled=st.session_state['completion_time'] is not None and not st.session_state['admin_access'])
num_deliveries = st.number_input('배달 총 개수:', min_value=0, disabled=st.session_state['completion_time'] is not None and not st.session_state['admin_access'])

# Calculate total time
total_time = nav_time + (5 * num_deliveries)

if st.button('예상배달시간 계산'):
    current_time_utc = datetime.now(pytz.utc)
    kst = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst)
    completion_time_kst = current_time_kst + timedelta(minutes=total_time)
    st.session_state['completion_time'] = completion_time_kst

# Countdown display
countdown_container = st.empty()  # Create a placeholder for countdown

# Function to update countdown
def update_countdown():
    while True:
        current_time = datetime.now(pytz.timezone('Asia/Seoul'))
        if 'completion_time' in st.session_state and st.session_state['completion_time'] is not None:
            time_remaining = st.session_state['completion_time'] - current_time
            
            if time_remaining.total_seconds() > 0:
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                # Display the countdown
                countdown_container.markdown(f"""
                    <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                         {minutes:02} minutes, {seconds:02} seconds 안에 매장 복귀합니다
                    </div>
                """, unsafe_allow_html=True)
            else:
                countdown_container.markdown(f"""
                    <div style="font-size: 48px; text-align: center; color: #FF5733; font-weight: bold;">
                        곧 복귀합니다!
                    </div>
                """, unsafe_allow_html=True)
                break  # Exit the loop if time is up

        time.sleep(1)  # Wait for 1 second before the next update

# Start the countdown if a completion time exists
if st.session_state['completion_time'] is not None:
    update_countdown()

# Show password input if admin access is not granted and the calculation has been done
if st.session_state['completion_time'] is not None and not st.session_state['admin_access']:
    st.subheader("입력 필드를 수정하려면 비밀번호를 입력하세요.")
    check_password()
