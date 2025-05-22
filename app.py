from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from components.auth import init_auth, show_auth_modal
from components.dashboard import show_dashboard
from components.interview import show_interview
from components.results import show_results
from utils.db_utils import init_db
from utils.auth_utils import init_auth_session

# Set page config
st.set_page_config(
    page_title="Data Science Interview Simulator",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🎯"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    /* Modern Design System */
    :root {
        /* Brand Colors */
        --brand-primary: #2563EB;
        --brand-secondary: #3B82F6;
        --brand-accent: #60A5FA;

        /* Neutral Colors */
        --neutral-50: #F8FAFC;
        --neutral-100: #F1F5F9;
        --neutral-200: #E2E8F0;
        --neutral-300: #CBD5E1;
        --neutral-400: #94A3B8;
        --neutral-500: #64748B;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1E293B;
        --neutral-900: #0F172A;

        /* Semantic Colors */
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --info: #3B82F6;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--neutral-50);
        color: var(--neutral-900);
        font-family: system-ui, -apple-system, sans-serif;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1rem;
        color: var(--neutral-900);
    }

    /* Card Styles */
    .card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        transition: all 0.3s ease;
        border: 1px solid var(--neutral-200);
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }

    /* Button Styles */
    .stButton > button {
        background: var(--brand-primary);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: var(--brand-secondary);
        transform: translateY(-1px);
    }

    /* Input Styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid var(--neutral-300);
        border-radius: 0.5rem;
        padding: 0.75rem;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--brand-primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    /* Error Message Styles */
    .stAlert {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
        color: #DC2626 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    .stAlert p {
        color: #DC2626 !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    /* Success Message Styles */
    .stSuccess {
        background-color: #D1FAE5 !important;
        border: 1px solid #A7F3D0 !important;
        color: #059669 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    .stSuccess p {
        color: #059669 !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    /* Warning Message Styles */
    .stWarning {
        background-color: #FEF3C7 !important;
        border: 1px solid #FCD34D !important;
        color: #D97706 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    .stWarning p {
        color: #D97706 !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    # Initialize database and auth
    init_db()
    init_auth_session()
    st.session_state['initialized'] = True

if 'interview_started' not in st.session_state:
    st.session_state['interview_started'] = False
if 'interview_completed' not in st.session_state:
    st.session_state['interview_completed'] = False

# Main application flow
def main():
    # Show login modal if needed
    if st.session_state.get('show_login', False):
        show_auth_modal()
        st.stop()

    # Main content routing
    if not st.session_state['interview_started']:
        show_dashboard()
    elif st.session_state['interview_started'] and not st.session_state['interview_completed']:
        show_interview()
    else:
        show_results()

if __name__ == "__main__":
    main()