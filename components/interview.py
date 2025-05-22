import streamlit as st
import time
from components.timer import show_timer
from components.question import show_question
from components.feedback import show_feedback
from utils.interview_utils import get_random_question, evaluate_answer, get_ai_response
from db_utils import create_interview, save_question_response, update_interview_score

def show_interview():
    """Show the interview interface"""
    # Initialize session state for interview
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = None
    if 'current_answer' not in st.session_state:
        st.session_state['current_answer'] = None
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = []
    if 'evaluations' not in st.session_state:
        st.session_state['evaluations'] = []
    if 'question_count' not in st.session_state:
        st.session_state['question_count'] = 0
    if 'show_qa' not in st.session_state:
        st.session_state['show_qa'] = False
    if 'user_questions' not in st.session_state:
        st.session_state['user_questions'] = []
    if 'ai_responses' not in st.session_state:
        st.session_state['ai_responses'] = []
    if 'current_evaluation' not in st.session_state:
        st.session_state['current_evaluation'] = None
    if 'interview_completed' not in st.session_state:
        st.session_state['interview_completed'] = False
    if 'show_next_button' not in st.session_state:
        st.session_state['show_next_button'] = False
    if 'answer_key' not in st.session_state:
        st.session_state['answer_key'] = 0
    if 'interview_id' not in st.session_state:
        st.session_state['interview_id'] = None
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = time.time()
    if 'show_results' not in st.session_state:
        st.session_state['show_results'] = False

    # Display user info and progress
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f"### 👤 {st.session_state['name']}")
    with col2:
        if not st.session_state['interview_completed']:
            st.markdown(f"### 📝 Question {st.session_state['question_count'] + 1} of 5")
        else:
            st.markdown("### ✅ Interview Completed")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            from utils.auth_utils import logout
            logout()
            st.rerun()

    st.divider()

    # Create interview in database if not exists
    if st.session_state['interview_id'] is None:
        interview_id = create_interview(
            st.session_state['user_id'],
            st.session_state['selected_category']
        )
        if interview_id:
            st.session_state['interview_id'] = interview_id

    # Timer
    if 'start_time' in st.session_state:
        elapsed_time = time.time() - st.session_state['start_time']
        remaining_time = 300 - elapsed_time  # 5 minutes per question
        
        if remaining_time <= 0:
            st.warning("Time's up! Moving to the next question...")
            st.session_state['question_count'] += 1
            if st.session_state['question_count'] >= 5:
                st.session_state['interview_completed'] = True
                st.session_state['show_qa'] = True
                st.session_state['show_results'] = True
                st.rerun()
            else:
                st.session_state['current_question'], st.session_state['current_answer'] = get_random_question(st.session_state['selected_category'])
                st.session_state['start_time'] = time.time()
                st.session_state['answer_key'] += 1
                st.rerun()
        
        st.progress(remaining_time / 300)
        st.write(f"Time remaining: {int(remaining_time)} seconds")

    # Show current question
    if st.session_state['current_question']:
        st.markdown("### Current Question")
        st.write(st.session_state['current_question'])
        
        # Answer input with unique key
        user_answer = st.text_area("Your Answer", height=200, key=f"answer_{st.session_state['answer_key']}")
        
        if st.button("Submit Answer"):
            if user_answer:
                # Evaluate answer
                evaluation = evaluate_answer(
                    st.session_state['current_question'],
                    user_answer,
                    st.session_state['current_answer']
                )
                
                # Store answer and evaluation
                st.session_state['user_answers'].append(user_answer)
                st.session_state['evaluations'].append(evaluation)
                st.session_state['current_evaluation'] = evaluation
                st.session_state['show_next_button'] = True

                # Save response to database
                if st.session_state['interview_id']:
                    # Parse evaluation to get score
                    evaluation_lines = evaluation.split('\n')
                    score = 0
                    for line in evaluation_lines:
                        if line.startswith('Score:'):
                            try:
                                score = float(line.split(':')[1].split('/')[0].strip())
                                break
                            except:
                                continue

                    save_question_response(
                        st.session_state['interview_id'],
                        st.session_state['current_question'],
                        user_answer,
                        st.session_state['current_answer'],
                        score,
                        evaluation,
                        int(time.time() - st.session_state['start_time'])
                    )

                st.rerun()
            else:
                st.error("Please provide an answer before submitting.")

        # Show current evaluation if it exists
        if st.session_state['current_evaluation']:
            st.markdown("### Evaluation")
            
            # Parse the evaluation response
            evaluation_lines = st.session_state['current_evaluation'].split('\n')
            score = ""
            strengths = []
            improvements = []
            ideal_response = ""
            
            current_section = None
            for line in evaluation_lines:
                if line.startswith('Score:'):
                    score = line.replace('Score:', '').strip()
                elif line.startswith('Strengths:'):
                    current_section = 'strengths'
                elif line.startswith('Improvements:'):
                    current_section = 'improvements'
                elif line.startswith('Ideal Response:'):
                    current_section = 'ideal'
                elif line.strip() and current_section:
                    if current_section == 'strengths':
                        strengths.append(line.strip())
                    elif current_section == 'improvements':
                        improvements.append(line.strip())
                    elif current_section == 'ideal':
                        ideal_response += line.strip() + ' '
            
            # Display score
            st.markdown(f"### Score: {score}")
            
            # Display strengths
            if strengths:
                st.markdown("#### Key Strengths")
                for strength in strengths:
                    st.markdown(f"✅ {strength}")
            
            # Display improvements
            if improvements:
                st.markdown("#### Areas for Improvement")
                for improvement in improvements:
                    st.markdown(f"💡 {improvement}")
            
            # Display ideal response
            if ideal_response:
                st.markdown("#### Ideal Response")
                st.markdown(ideal_response)
            
            st.divider()

            # Show Next Question button
            if st.session_state['show_next_button']:
                if st.button("Next Question"):
                    st.session_state['question_count'] += 1
                    if st.session_state['question_count'] >= 5:
                        st.session_state['interview_completed'] = True
                        st.session_state['show_qa'] = True
                        st.session_state['show_results'] = True
                        
                        # Update final interview score
                        if st.session_state['interview_id']:
                            total_score = 0
                            for evaluation in st.session_state['evaluations']:
                                try:
                                    score_line = evaluation.split('\n')[0]
                                    score = float(score_line.split(':')[1].split('/')[0].strip())
                                    total_score += score
                                except:
                                    continue
                            
                            avg_score = total_score / len(st.session_state['evaluations'])
                            update_interview_score(
                                st.session_state['interview_id'],
                                avg_score,
                                len(st.session_state['evaluations'])
                            )
                    else:
                        st.session_state['current_question'], st.session_state['current_answer'] = get_random_question(st.session_state['selected_category'])
                        st.session_state['start_time'] = time.time()
                    st.session_state['current_evaluation'] = None
                    st.session_state['show_next_button'] = False
                    st.session_state['answer_key'] += 1  # Increment key to clear text area
                    st.rerun()

    # Q&A Section after completing 5 questions
    if st.session_state['show_qa']:
        st.markdown("""
            <div style='
                background: white;
                padding: 2rem;
                border-radius: 1rem;
                border: 2px solid var(--brand-primary);
                margin: 2rem 0;
            '>
                <h2 style='color: var(--brand-primary); margin-bottom: 1rem;'>
                    🤖 Ask the AI Assistant
                </h2>
                <p style='color: var(--neutral-600); margin-bottom: 1rem;'>
                    You can ask up to 3 questions about data science topics. The AI will provide detailed answers to help you learn.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if len(st.session_state['user_questions']) < 3:
            user_question = st.text_input("Your Question")
            if st.button("Ask Question"):
                if user_question:
                    # Get AI response
                    ai_response = get_ai_response(user_question)
                    
                    # Store question and response
                    st.session_state['user_questions'].append(user_question)
                    st.session_state['ai_responses'].append(ai_response)
                    
                    # Show response
                    st.markdown("### AI Response")
                    st.write(ai_response)
                else:
                    st.error("Please enter a question.")
        
        # Show all Q&A
        if st.session_state['user_questions']:
            st.markdown("### Your Questions and Answers")
            for i, (question, response) in enumerate(zip(st.session_state['user_questions'], st.session_state['ai_responses'])):
                st.markdown(f"**Question {i+1}:** {question}")
                st.markdown(f"**Answer:** {response}")
                st.divider()
        
        if len(st.session_state['user_questions']) >= 3:
            st.info("You've asked all your questions. Click below to see your interview results.")
            if st.button("View Results"):
                st.session_state['show_results'] = True
                st.rerun()

    # Show interview results
    if st.session_state['show_results']:
        st.markdown("### 📊 Interview Results")
        
        if st.session_state['evaluations']:
            # Calculate average score
            total_score = 0
            for evaluation in st.session_state['evaluations']:
                try:
                    score_line = evaluation.split('\n')[0]
                    score = int(score_line.split(':')[1].split('/')[0].strip())
                    total_score += score
                except:
                    continue
            
            avg_score = total_score / len(st.session_state['evaluations'])
            
            # Display overall score
            st.markdown(f"#### Overall Score: {avg_score:.1f}/10")
            
            # Display all questions and answers
            st.markdown("#### Question-by-Question Breakdown")
            for i, (question, answer, evaluation) in enumerate(zip(
                st.session_state['current_question'] if isinstance(st.session_state['current_question'], list) else [st.session_state['current_question']],
                st.session_state['user_answers'],
                st.session_state['evaluations']
            )):
                st.markdown(f"**Question {i+1}:** {question}")
                st.markdown(f"**Your Answer:** {answer}")
                st.markdown("**Evaluation:**")
                st.markdown(evaluation)
                st.divider()
            
            # Display Q&A section
            if st.session_state['user_questions']:
                st.markdown("#### Your Questions and Answers")
                for i, (question, response) in enumerate(zip(st.session_state['user_questions'], st.session_state['ai_responses'])):
                    st.markdown(f"**Question {i+1}:** {question}")
                    st.markdown(f"**Answer:** {response}")
                    st.divider()
        else:
            st.error("No interview results found. Please complete an interview first.")
