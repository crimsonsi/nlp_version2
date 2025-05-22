import streamlit as st
import pandas as pd
from pathlib import Path
from components.auth import show_auth_buttons
from utils.interview_utils import get_random_question
import time

from components.history import show_history

def show_dashboard():
    """Show the main dashboard"""
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1 style='color: var(--brand-primary);'>Interview Simulator</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎯 Start Interview", "📚 History"])
    
    with tab1:
        categories = ["All", "Machine Learning", "Data Analysis", "Statistics", "Python", "SQL"]
        st.session_state['selected_category'] = st.selectbox(
            "Choose Interview Category",
            categories,
            index=0
        )
        
        if st.button("Start Interview", use_container_width=True):
            st.session_state['page'] = 'interview'
            st.rerun()
            
    with tab2:
        show_history()

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
    """Show the main dashboard with interview options"""
    show_auth_buttons()

    # Welcome message for logged-in users
    if st.session_state.get('is_authenticated'):
        st.markdown(f"""
        <div style="text-align:center; margin-bottom: 1rem;">
            <h2 style="color: var(--brand-primary); font-size:1.5rem;">Welcome back, {st.session_state['name']}! 👋</h2>
        </div>
        """, unsafe_allow_html=True)

    # Logo and Title
    st.markdown("""
    <div style="text-align:center; margin-bottom: 2rem;">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="80" style="margin-bottom: 1rem;" />
        <h1 style="font-size:2.5rem; font-weight:800; color:var(--brand-primary); margin-bottom:0.5rem;">Data Science Interview Simulator</h1>
        <p style="font-size:1.2rem; color:var(--neutral-700);">Practice. Improve. Succeed.</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Card
    with st.container():
        st.markdown("""
        <div style="background: white; border-radius: 1.5rem; box-shadow: 0 4px 24px rgba(37,99,235,0.07); padding: 2.5rem 2rem; margin-bottom: 2rem;">
        """, unsafe_allow_html=True)
        
        # Hero Section
        st.markdown("""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h2 style="color: var(--brand-primary); font-size:2rem; font-weight:700;">Master Your Interview Skills 🚀</h2>
            <p style="font-size:1.1rem; color:var(--neutral-700); max-width:600px; margin:0 auto;">Practice with our AI-powered interview simulator and get real-time feedback on your answers.</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Features Section
        st.markdown("<h3 style='text-align:center; color:var(--brand-primary); margin-bottom:2rem;'>Key Features</h3>", unsafe_allow_html=True)
        feature_cols = st.columns(3)
        features = [
            ("⏱️", "Smart Timing", "Practice with realistic time limits and learn to manage your interview responses effectively."),
            ("💡", "AI Feedback", "Get instant, detailed feedback on your answers using advanced natural language processing."),
            ("📊", "Performance Analytics", "Track your progress and identify areas for improvement with detailed analytics.")
        ]
        for i, (icon, title, desc) in enumerate(features):
            with feature_cols[i]:
                st.markdown(f"""
                <div style='background:var(--neutral-50); border-radius:1rem; padding:1.5rem; text-align:center; box-shadow:0 2px 8px rgba(37,99,235,0.04); margin-bottom:1rem;'>
                    <div style='font-size:2.5rem; margin-bottom:0.5rem;'>{icon}</div>
                    <div style='font-weight:700; color:var(--brand-primary); font-size:1.1rem; margin-bottom:0.5rem;'>{title}</div>
                    <div style='color:var(--neutral-700); font-size:1rem;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # Interview Format
        st.markdown("<h4 style='color:var(--brand-primary); margin-bottom:1rem;'>Interview Format</h4>", unsafe_allow_html=True)
        format_cols = st.columns(4)
        formats = [
            ("⏱️", "Time Limit", "5 minutes per question"),
            ("🎯", "Questions", "5 per session"),
            ("💡", "Feedback", "Instant scoring"),
            ("📊", "Analytics", "Detailed metrics")
        ]
        for i, (icon, title, desc) in enumerate(formats):
            with format_cols[i]:
                st.markdown(f"""
                <div style='background:var(--neutral-100); border-radius:0.75rem; padding:1rem; text-align:center;'>
                    <div style='font-size:1.5rem; margin-bottom:0.25rem;'>{icon}</div>
                    <div style='font-weight:600; color:var(--brand-primary); font-size:1rem;'>{title}</div>
                    <div style='color:var(--neutral-700); font-size:0.95rem;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # Category Selection
        st.markdown("<h4 style='color:var(--brand-primary); margin-bottom:0.5rem;'>Choose Your Interview Category</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color:var(--neutral-700); margin-bottom:1rem;'>Select the category you want to practice with. Each category focuses on different aspects of data science interviews.</p>", unsafe_allow_html=True)
        data = load_data()
        if data is not None:
            categories = ["All"] + list(data['Category'].unique())
            selected_category = st.selectbox(
                "Interview Category",
                categories,
                format_func=lambda x: "📚 " + x if x != "All" else "📚 All Categories",
                index=0,
                key="dashboard_category_select"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
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
        st.markdown("</div>", unsafe_allow_html=True)
