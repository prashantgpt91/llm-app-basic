import streamlit as st
import cv2
import time
from PIL import Image

# Title of the app
st.title("Aarogya AHC")

# Initialize session state if not already done
if 'timer_started' not in st.session_state:
    st.session_state.timer_started = False
    st.session_state.end_time = 0

# Function to start or restart the timer
def start_timer():
    st.session_state.start_time = time.time()
    st.session_state.end_time = st.session_state.start_time + 40  # 40 second timer
    st.session_state.timer_started = True

st.markdown("""
    <style>
    .start-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .start-btn:hover {
        background-color: #45a049;
    }
    .restart-btn {
        background-color: #f44336;
        color: white;
        padding: 10px 24px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .restart-btn:hover {
        background-color: #da190b;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Vital Collection", key='start'):
        start_timer()

with col2:
    if st.button("Restart Session", key='restart'):
        start_timer()

# Apply custom styles to buttons
st.markdown("""
    <script>
    document.querySelectorAll('.stButton button')[0].classList.add('start-btn');
    document.querySelectorAll('.stButton button')[1].classList.add('restart-btn');
    </script>
    """, unsafe_allow_html=True)

if st.session_state.timer_started:
    cap = cv2.VideoCapture(0)
    timer_container = st.empty()
    video_container = st.empty()
    
    while True:
        current_time = time.time()
        remaining_time = int(st.session_state.end_time - current_time)
        
        if remaining_time > 0:
            timer_container.write(f"Time remaining: {remaining_time} seconds")
            
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            video_container.image(img, caption="Webcam Feed", use_column_width=True)
            
            time.sleep(0.1)  
        else:
            timer_container.write("Time is up!")
            st.write("Thank you")
            st.session_state.timer_started = False
            cap.release()
            break
