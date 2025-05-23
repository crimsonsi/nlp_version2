import streamlit as st
from db_utils import get_interview_responses
from utils.interview_utils import get_ai_response

def show_results():
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        '>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>🎉 Interview Complete!</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Here's how you performed</p>
        </div>
    """, unsafe_allow_html=True)

    # Calculate overall score
    if st.session_state.get('evaluations'):
        total_score = 0
        for evaluation in st.session_state['evaluations']:
            try:
                score_line = evaluation.split('\n')[0]
                score = float(score_line.split(':')[1].split('/')[0].strip())
                total_score += score
            except:
                continue

        avg_score = total_score / len(st.session_state['evaluations'])

        # Display score card
        st.markdown(f"""
            <div style='
                background: white;
                border-radius: 1rem;
                padding: 2rem;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            '>
                <h2 style='color: var(--brand-primary); font-size: 3rem; margin-bottom: 0.5rem;'>{avg_score:.1f}/10</h2>
                <p style='color: var(--neutral-600); font-size: 1.2rem;'>Overall Score</p>
            </div>
        """, unsafe_allow_html=True)

        # Display detailed breakdown
        st.markdown("""
            <h3 style='color: var(--brand-primary); margin-bottom: 1.5rem;'>
                📊 Detailed Performance Breakdown
            </h3>
        """, unsafe_allow_html=True)

        for i, (question, answer, evaluation) in enumerate(zip(
            st.session_state['current_question'] if isinstance(st.session_state['current_question'], list) else [st.session_state['current_question']],
            st.session_state['user_answers'],
            st.session_state['evaluations']
        )):
            with st.expander(f"Question {i+1} Details"):
                st.markdown(f"""
                    <div style='
                        background: var(--neutral-50);
                        border-radius: 0.75rem;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                    '>
                        <h4 style='color: var(--brand-primary); margin-bottom: 1rem;'>Question</h4>
                        <p style='color: var(--neutral-800); font-size: 1.1rem;'>{question}</p>

                        <h4 style='color: var(--brand-primary); margin: 1rem 0;'>Your Answer</h4>
                        <div style='
                            background: white;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            border: 1px solid var(--neutral-200);
                        '>
                            <p style='color: var(--neutral-800);'>{answer}</p>
                        </div>

                        <h4 style='color: var(--brand-primary); margin: 1rem 0;'>Evaluation</h4>
                        <div style='
                            background: white;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            border: 1px solid var(--neutral-200);
                        '>
                            <p style='color: var(--neutral-800); white-space: pre-line;'>{evaluation}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # Display Q&A section
        if st.session_state.get('user_questions'):
            st.markdown("""
                <h3 style='color: var(--brand-primary); margin: 2rem 0 1.5rem;'>
                    💡 Your Q&A Session
                </h3>
            """, unsafe_allow_html=True)

            for i, (question, response) in enumerate(zip(
                st.session_state['user_questions'],
                st.session_state['ai_responses']
            )):
                with st.expander(f"Q&A {i+1}"):
                    st.markdown(f"""
                        <div style='
                            background: var(--neutral-50);
                            border-radius: 0.75rem;
                            padding: 1.5rem;
                            margin-bottom: 1rem;
                        '>
                            <h4 style='color: var(--brand-primary); margin-bottom: 0.5rem;'>Your Question</h4>
                            <p style='color: var(--neutral-800); font-size: 1.1rem;'>{question}</p>

                            <h4 style='color: var(--brand-primary); margin: 1rem 0 0.5rem;'>AI Response</h4>
                            <p style='color: var(--neutral-800);'>{response}</p>
                        </div>
                    """, unsafe_allow_html=True)

        # Q&A Section
        st.markdown("""
            <div style='
                background: white;
                border-radius: 1rem;
                padding: 2rem;
                margin: 2rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border: 1px solid var(--neutral-200);
            '>
                <h3 style='color: var(--brand-primary); margin-bottom: 1rem;'>
                    🤖 Ask the AI Assistant
                </h3>
                <p style='color: var(--neutral-600); margin-bottom: 1rem;'>
                    You can ask up to 3 questions about any data science topic
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Show remaining questions counter
        questions_asked = len(st.session_state.get('user_questions', []))
        questions_remaining = 3 - questions_asked
        
        if questions_remaining > 0:
            st.markdown(f"""
                <div style='
                    background: var(--neutral-50);
                    padding: 0.75rem;
                    border-radius: 0.5rem;
                    text-align: center;
                    margin-bottom: 1rem;
                '>
                    <p style='color: var(--neutral-600); margin: 0;'>
                        ⭐️ {questions_remaining} questions remaining
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            question = st.text_area(
                "Your Question",
                height=100,
                placeholder="Ask anything about data science, algorithms, or interview preparation...",
                key="qa_input"
            )
            
            if st.button("🚀 Ask Question", type="primary", use_container_width=True):
                if question:
                    with st.spinner("Getting AI response..."):
                        ai_response = get_ai_response(question)
                        if 'user_questions' not in st.session_state:
                            st.session_state['user_questions'] = []
                        if 'ai_responses' not in st.session_state:
                            st.session_state['ai_responses'] = []
                        st.session_state['user_questions'].append(question)
                        st.session_state['ai_responses'].append(ai_response)
                        st.rerun()
                else:
                    st.error("Please enter a question first!")
        else:
            st.info("You've used all your questions! Check out the responses below.")

        st.divider()

        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Start New Interview", use_container_width=True):
                st.session_state['interview_started'] = False
                st.session_state['interview_completed'] = False
                st.session_state['show_results'] = False
                st.rerun()

        with col2:
            if st.button("📊 View History", use_container_width=True):
                st.session_state['page'] = 'history'
                st.rerun()
    else:
        st.error("No interview results found. Please complete an interview first.")