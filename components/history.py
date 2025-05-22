
import streamlit as st
from utils.db_utils import get_user_interviews, get_interview_responses

def show_history():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='color: var(--brand-primary);'>📚 Interview History</h2>
        </div>
    """, unsafe_allow_html=True)
    
    interviews = get_user_interviews(st.session_state['user_id'])
    
    if not interviews:
        st.info("You haven't completed any interviews yet.")
        return
        
    for interview in interviews:
        with st.expander(f"Interview on {interview['completed_at'].strftime('%Y-%m-%d %H:%M')} - Score: {interview['score']:.1f}/10"):
            responses = get_interview_responses(interview['id'])
            
            for i, response in enumerate(responses, 1):
                st.markdown(f"""
                    <div style='
                        background: white;
                        padding: 1.5rem;
                        border-radius: 0.5rem;
                        margin: 1rem 0;
                        border-left: 4px solid var(--brand-primary);
                    '>
                        <p style='color: var(--brand-primary); font-weight: 600;'>Question {i}</p>
                        <p style='margin: 0.5rem 0;'>{response['question']}</p>
                        <p style='color: var(--neutral-600); margin-top: 1rem;'>Your Answer:</p>
                        <p style='background: #f8f9fa; padding: 0.5rem; border-radius: 0.25rem;'>{response['user_answer']}</p>
                        <p style='color: var(--neutral-600); margin-top: 1rem;'>Score: {response['score']}/10</p>
                        <p style='color: var(--neutral-600); margin-top: 0.5rem;'>Time taken: {response['time_taken']} seconds</p>
                    </div>
                """, unsafe_allow_html=True)
