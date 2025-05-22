import streamlit as st
from db_utils import get_interview_responses

def show_results():
    """Show interview results"""
    st.markdown("### 📊 Interview Results")
    
    if 'interview_id' in st.session_state and st.session_state['interview_id']:
        # Get interview responses from database
        responses = get_interview_responses(st.session_state['interview_id'])
        
        if responses:
            # Calculate average score
            total_score = sum(response['score'] for response in responses)
            avg_score = total_score / len(responses)
            
            # Display overall score
            st.markdown(f"#### Overall Score: {avg_score:.1f}/10")
            
            # Display all questions and answers
            st.markdown("#### Question-by-Question Breakdown")
            for i, response in enumerate(responses, 1):
                st.markdown(f"**Question {i}:** {response['question']}")
                st.markdown(f"**Your Answer:** {response['user_answer']}")
                st.markdown("**Evaluation:**")
                st.markdown(response['feedback'])
                st.divider()
            
            # Display Q&A section
            if st.session_state.get('user_questions'):
                st.markdown("#### Your Questions and Answers")
                for i, (question, response) in enumerate(zip(st.session_state['user_questions'], st.session_state['ai_responses'])):
                    st.markdown(f"**Question {i+1}:** {question}")
                    st.markdown(f"**Answer:** {response}")
                    st.divider()
        else:
            st.error("No interview results found. Please complete an interview first.")
    else:
        st.error("No interview results found. Please complete an interview first.")
