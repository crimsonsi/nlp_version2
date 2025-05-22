
import streamlit as st
from utils.db_utils import get_user_interviews, get_interview_responses
from datetime import datetime

def show_history():
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        '>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📚 Interview History</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Track your progress and improvement over time</p>
        </div>
    """, unsafe_allow_html=True)
    
    interviews = get_user_interviews(st.session_state['user_id'])
    
    if not interviews:
        st.info("You haven't completed any interviews yet. Start one now to build your history!")
        if st.button("🎯 Start Your First Interview", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()
        return
    
    # Display interview history cards
    for interview in interviews:
        with st.container():
            st.markdown(f"""
                <div style='
                    background: white;
                    border-radius: 1rem;
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                '>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                        <div>
                            <h3 style='color: var(--brand-primary); margin: 0;'>
                                Interview on {interview['completed_at'].strftime('%B %d, %Y')}
                            </h3>
                            <p style='color: var(--neutral-600); margin: 0.25rem 0 0 0;'>
                                {interview['completed_at'].strftime('%I:%M %p')}
                            </p>
                        </div>
                        <div style='
                            background: var(--neutral-50);
                            padding: 0.5rem 1rem;
                            border-radius: 0.5rem;
                            text-align: center;
                        '>
                            <h4 style='color: var(--brand-primary); margin: 0; font-size: 1.5rem;'>
                                {interview['score']:.1f}/10
                            </h4>
                            <p style='color: var(--neutral-600); margin: 0; font-size: 0.875rem;'>Score</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            responses = get_interview_responses(interview['id'])
            with st.expander("View Details"):
                for i, response in enumerate(responses, 1):
                    st.markdown(f"""
                        <div style='
                            background: var(--neutral-50);
                            border-radius: 0.75rem;
                            padding: 1.5rem;
                            margin: 1rem 0;
                        '>
                            <h4 style='color: var(--brand-primary); margin-bottom: 1rem;'>Question {i}</h4>
                            <p style='color: var(--neutral-800); margin-bottom: 1rem;'>{response['question']}</p>
                            
                            <h5 style='color: var(--neutral-700); margin-bottom: 0.5rem;'>Your Answer</h5>
                            <div style='
                                background: white;
                                padding: 1rem;
                                border-radius: 0.5rem;
                                margin-bottom: 1rem;
                                border: 1px solid var(--neutral-200);
                            '>
                                <p style='color: var(--neutral-800); margin: 0;'>{response['user_answer']}</p>
                            </div>
                            
                            <div style='
                                display: flex;
                                justify-content: space-between;
                                background: var(--neutral-100);
                                padding: 0.75rem;
                                border-radius: 0.5rem;
                            '>
                                <span style='color: var(--neutral-700);'>
                                    Score: <strong>{response['score']}/10</strong>
                                </span>
                                <span style='color: var(--neutral-700);'>
                                    Time: <strong>{response['time_taken']} seconds</strong>
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Start New Interview", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            show_analytics(interviews)

def show_analytics(interviews):
    st.markdown("""
        <h2 style='color: var(--brand-primary); margin: 2rem 0 1rem;'>📈 Performance Analytics</h2>
    """, unsafe_allow_html=True)
    
    # Calculate statistics
    scores = [interview['score'] for interview in interviews]
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    total_interviews = len(interviews)
    
    # Display statistics cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div style='
                background: white;
                border-radius: 1rem;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            '>
                <h3 style='color: var(--brand-primary); margin: 0;'>{avg_score:.1f}/10</h3>
                <p style='color: var(--neutral-600); margin: 0.5rem 0 0 0;'>Average Score</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='
                background: white;
                border-radius: 1rem;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            '>
                <h3 style='color: var(--brand-primary); margin: 0;'>{max_score:.1f}/10</h3>
                <p style='color: var(--neutral-600); margin: 0.5rem 0 0 0;'>Best Score</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='
                background: white;
                border-radius: 1rem;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            '>
                <h3 style='color: var(--brand-primary); margin: 0;'>{total_interviews}</h3>
                <p style='color: var(--neutral-600); margin: 0.5rem 0 0 0;'>Total Interviews</p>
            </div>
        """, unsafe_allow_html=True)
