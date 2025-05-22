
import streamlit as st
from db_utils import get_interview_responses

def show_results():
    """Show interview results with improved UI"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h2 style='color: var(--brand-primary);'>📊 Interview Results</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if 'interview_id' in st.session_state and st.session_state['interview_id']:
        responses = get_interview_responses(st.session_state['interview_id'])
        
        if responses:
            # Calculate average score
            total_score = sum(response['score'] for response in responses)
            avg_score = total_score / len(responses)
            
            # Display overall score with improved UI
            st.markdown(f"""
                <div style='
                    background: var(--gradient-primary);
                    border-radius: var(--radius-xl);
                    padding: 2rem;
                    text-align: center;
                    color: white;
                    margin-bottom: 2rem;
                '>
                    <h3>Overall Performance</h3>
                    <div style='font-size: 3rem; font-weight: bold;'>
                        {avg_score:.1f}/10
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Display detailed breakdown
            st.markdown("""
                <h3 style='color: var(--neutral-800); margin-bottom: 1.5rem;'>
                    Question-by-Question Breakdown
                </h3>
            """, unsafe_allow_html=True)
            
            for i, response in enumerate(responses, 1):
                st.markdown(f"""
                    <div style='
                        background: white;
                        border-radius: var(--radius-lg);
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        border: 1px solid var(--neutral-200);
                    '>
                        <div style='color: var(--brand-primary); font-weight: 600; margin-bottom: 0.5rem;'>
                            Question {i}
                        </div>
                        <div style='color: var(--neutral-800); font-size: 1.1rem; margin-bottom: 1rem;'>
                            {response['question']}
                        </div>
                        <div style='
                            background: var(--neutral-50);
                            padding: 1rem;
                            border-radius: var(--radius-md);
                            margin-bottom: 1rem;
                        '>
                            <div style='color: var(--neutral-600); font-weight: 500; margin-bottom: 0.5rem;'>
                                Your Answer:
                            </div>
                            <div style='color: var(--neutral-800);'>
                                {response['user_answer']}
                            </div>
                        </div>
                        <div style='
                            border-left: 4px solid var(--brand-primary);
                            padding-left: 1rem;
                        '>
                            <div style='color: var(--neutral-600); font-weight: 500; margin-bottom: 0.5rem;'>
                                Feedback:
                            </div>
                            <div style='color: var(--neutral-800);'>
                                {response['feedback']}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Q&A Section
            if st.session_state.get('user_questions'):
                st.markdown("""
                    <h3 style='
                        color: var(--neutral-800);
                        margin: 2rem 0 1.5rem 0;
                        padding-top: 2rem;
                        border-top: 1px solid var(--neutral-200);
                    '>
                        Your Questions & Answers
                    </h3>
                """, unsafe_allow_html=True)
                
                for i, (question, response) in enumerate(zip(
                    st.session_state['user_questions'],
                    st.session_state['ai_responses']
                ), 1):
                    st.markdown(f"""
                        <div style='
                            background: white;
                            border-radius: var(--radius-lg);
                            padding: 1.5rem;
                            margin-bottom: 1rem;
                            border: 1px solid var(--neutral-200);
                        '>
                            <div style='color: var(--brand-primary); font-weight: 600; margin-bottom: 0.5rem;'>
                                Question {i}
                            </div>
                            <div style='color: var(--neutral-800); font-size: 1.1rem; margin-bottom: 1rem;'>
                                {question}
                            </div>
                            <div style='
                                background: var(--neutral-50);
                                padding: 1rem;
                                border-radius: var(--radius-md);
                            '>
                                <div style='color: var(--neutral-600); font-weight: 500; margin-bottom: 0.5rem;'>
                                    Answer:
                                </div>
                                <div style='color: var(--neutral-800);'>
                                    {response}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("No interview results found. Please complete an interview first.")
    else:
        st.error("No interview results found. Please complete an interview first.")
