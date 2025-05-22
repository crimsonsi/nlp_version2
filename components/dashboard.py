
import streamlit as st
import pandas as pd
from pathlib import Path
from components.auth import show_auth_buttons
from utils.interview_utils import get_random_question
import time
from components.history import show_history

def load_data():
    """Load interview questions data"""
    try:
        current_dir = Path(__file__).parent.parent
        data_path = current_dir / 'interview_qa_combined.csv'
        
        if not data_path.exists():
            st.error(f"Data file not found at {data_path}")
            return None
            
        df = pd.read_csv(data_path)
        if df.empty:
            st.error("The dataset is empty")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def show_dashboard():
    """Show the main dashboard with enhanced UI"""
    show_auth_buttons()

    # Header Section with Gradient Background
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 3rem;
            border-radius: 1rem;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            color: white;
        '>
            <h1 style='font-size: 3rem; font-weight: 800; margin-bottom: 1rem;'>
                Data Science Interview Master 🚀
            </h1>
            <p style='font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto;'>
                Practice real interview questions, get AI-powered feedback, and improve your skills
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Welcome message for logged-in users
    if st.session_state.get('is_authenticated'):
        st.markdown(f"""
            <div style='
                background: #F0F9FF;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 4px solid #3B82F6;
                margin-bottom: 2rem;
            '>
                <h3 style='color: #1E3A8A; margin: 0;'>👋 Welcome back, {st.session_state['name']}!</h3>
            </div>
        """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 1rem; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚡️</div>
                <h3 style='color: #1E3A8A; margin-bottom: 0.5rem;'>Real Questions</h3>
                <p style='color: #64748B; font-size: 0.9rem;'>Practice with industry-standard interview questions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 1rem; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🤖</div>
                <h3 style='color: #1E3A8A; margin-bottom: 0.5rem;'>AI Feedback</h3>
                <p style='color: #64748B; font-size: 0.9rem;'>Get instant, detailed feedback on your answers</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 1rem; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📈</div>
                <h3 style='color: #1E3A8A; margin-bottom: 0.5rem;'>Track Progress</h3>
                <p style='color: #64748B; font-size: 0.9rem;'>Monitor your improvement over time</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interview Categories Section
    st.markdown("""
        <div style='
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            margin: 2rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <h2 style='color: #1E3A8A; margin-bottom: 1rem; text-align: center;'>Choose Your Path 🎯</h2>
        </div>
    """, unsafe_allow_html=True)

    data = load_data()
    if data is not None:
        categories = ["All"] + list(data['Category'].unique())
        selected_category = st.selectbox(
            "Select Interview Category",
            categories,
            format_func=lambda x: f"📚 {x}",
            key="dashboard_category_select"
        )

        # Start Interview Button
        if st.button("🚀 Start Interview", use_container_width=True):
            if not st.session_state.get('is_authenticated'):
                st.session_state['show_login'] = True
                st.rerun()
            else:
                with st.spinner('🎯 Preparing your interview...'):
                    st.session_state['interview_started'] = True
                    st.session_state['selected_category'] = selected_category
                    st.session_state['current_question'], st.session_state['current_answer'] = get_random_question(selected_category)
                    st.session_state['start_time'] = time.time()
                    st.rerun()

    # Footer Section
    st.markdown("""
        <div style='
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: #64748B;
            border-top: 1px solid #E2E8F0;
        '>
            <p>Ready to ace your next data science interview? Start practicing now!</p>
        </div>
    """, unsafe_allow_html=True)
