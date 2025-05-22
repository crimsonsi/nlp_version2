import streamlit as st
import time

def show_timer():
    """Show the timer for the current question"""
    # Get start time from session state
    start_time = st.session_state.get('start_time', time.time())
    
    # Calculate time left (5 minutes = 300 seconds)
    time_left = 300 - (time.time() - start_time)
    
    # Format time left
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    
    # Show timer with color based on time left
    if time_left > 60:
        color = "green"
    elif time_left > 30:
        color = "orange"
    else:
        color = "red"
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        background-color: var(--neutral-50);
        margin: 10px 0;
    ">
        <h3 style="color: {color}; margin: 0;">
            ⏱️ Time Remaining: {minutes:02d}:{seconds:02d}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    return time_left
