
import streamlit as st
from db_utils import get_interview_responses

def show_results():
    """Show interview results with modern UI"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem; animation: fadeIn 0.5s ease-out;'>
            <h1 style='color: var(--brand-primary); font-size: 2.5rem; margin-bottom: 1rem;'>
                🎯 Interview Results
            </h1>
            <p style='color: var(--neutral-600); font-size: 1.2rem;'>
                Here's how you performed in your interview
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'interview_id' in st.session_state and st.session_state['interview_id']:
        responses = get_interview_responses(st.session_state['interview_id'])
        
        if responses:
            # Calculate metrics
            total_score = sum(response['score'] for response in responses)
            avg_score = total_score / len(responses)
            total_time = sum(response['time_taken'] for response in responses)
            
            # Display performance metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style='
                        background: white;
                        padding: 2rem;
                        border-radius: 1rem;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    '>
                        <h3 style='color: var(--brand-primary); margin-bottom: 0.5rem;'>
                            Overall Score
                        </h3>
                        <div style='font-size: 2.5rem; font-weight: bold; color: var(--brand-primary);'>
                            {avg_score:.1f}/10
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='
                        background: white;
                        padding: 2rem;
                        border-radius: 1rem;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    '>
                        <h3 style='color: var(--brand-primary); margin-bottom: 0.5rem;'>
                            Questions Answered
                        </h3>
                        <div style='font-size: 2.5rem; font-weight: bold; color: var(--brand-primary);'>
                            {len(responses)}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style='
                        background: white;
                        padding: 2rem;
                        border-radius: 1rem;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    '>
                        <h3 style='color: var(--brand-primary); margin-bottom: 0.5rem;'>
                            Total Time
                        </h3>
                        <div style='font-size: 2.5rem; font-weight: bold; color: var(--brand-primary);'>
                            {total_time//60}:{total_time%60:02d}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display detailed breakdown
            st.markdown("""
                <h2 style='color: var(--neutral-800); margin: 2rem 0 1rem 0;'>
                    Question Breakdown
                </h2>
            """, unsafe_allow_html=True)
            
            for i, response in enumerate(responses, 1):
                score_color = '#10B981' if response['score'] >= 7 else '#F59E0B' if response['score'] >= 5 else '#EF4444'
                st.markdown(f"""
                    <div style='
                        background: white;
                        border-radius: 1rem;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        border-left: 4px solid {score_color};
                    '>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                            <h3 style='color: var(--brand-primary); margin: 0;'>Question {i}</h3>
                            <div style='
                                background: {score_color};
                                color: white;
                                padding: 0.5rem 1rem;
                                border-radius: 2rem;
                                font-weight: 600;
                            '>
                                Score: {response['score']}/10
                            </div>
                        </div>
                        <div style='color: var(--neutral-800); font-size: 1.1rem; margin-bottom: 1rem;'>
                            {response['question']}
                        </div>
                        <div style='
                            background: var(--neutral-50);
                            padding: 1rem;
                            border-radius: 0.5rem;
                            margin-bottom: 0.5rem;
                        '>
                            <div style='color: var(--neutral-600); font-weight: 500; margin-bottom: 0.5rem;'>
                                Your Answer:
                            </div>
                            <div style='color: var(--neutral-800);'>
                                {response['user_answer']}
                            </div>
                        </div>
                        <div style='color: var(--neutral-600); font-size: 0.9rem; text-align: right;'>
                            Time taken: {response['time_taken']} seconds
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Back to Dashboard", use_container_width=True):
                    st.session_state['interview_started'] = False
                    st.session_state['interview_completed'] = False
                    st.rerun()
            with col2:
                if st.button("🎯 Start New Interview", use_container_width=True):
                    st.session_state['interview_started'] = False
                    st.session_state['interview_completed'] = False
                    st.session_state['current_question'] = None
                    st.session_state['current_answer'] = None
                    st.session_state['user_answers'] = []
                    st.session_state['evaluations'] = []
                    st.session_state['question_count'] = 0
                    st.rerun()
        else:
            st.error("No interview results found. Please complete an interview first.")
    else:
        st.error("No interview results found. Please complete an interview first.")
