import streamlit as st
from utils.auth_utils import login, logout, register

def init_auth():
    """Initialize authentication state"""
    if 'is_authenticated' not in st.session_state:
        st.session_state['is_authenticated'] = False
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

def show_auth():
    """Show authentication components"""
    # Initialize session state
    if 'is_authenticated' not in st.session_state:
        st.session_state['is_authenticated'] = False
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    # Show login/register forms if not authenticated
    if not st.session_state['is_authenticated']:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    success, msg = login(email, password)
                    if success:
                        st.session_state['is_authenticated'] = True
                        st.session_state['user_id'] = msg
                        st.rerun()
                    else:
                        st.error(msg)
        
        with tab2:
            with st.form("register_form"):
                first_name = st.text_input("First Name", key="register_first_name")
                last_name = st.text_input("Last Name", key="register_last_name")
                email = st.text_input("Email", key="register_email")
                password = st.text_input("Password", type="password", key="register_password")
                submitted = st.form_submit_button("Create Account")
                if submitted:
                    success, msg = register(first_name, last_name, email, password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    
    # Show logout button if authenticated
    else:
        st.write(f"Welcome, {st.session_state['name']}!")
        if st.button("Logout"):
            logout()
            st.rerun()

def show_auth_modal():
    """Show a simple login/register popup dialog"""
    st.markdown("""
        <style>
            .auth-container {
                background: white;
                border-radius: 0.75rem;
                box-shadow: 0 2px 12px rgba(0,0,0,0.1);
                padding: 1.5rem;
                margin: 1rem auto;
                width: 300px;
            }
            .auth-header {
                text-align: center;
                margin-bottom: 1.5rem;
            }
            .auth-title {
                color: var(--brand-primary);
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 0.25rem;
            }
            .auth-subtitle {
                color: var(--neutral-700);
                font-size: 0.875rem;
            }
            .auth-divider {
                text-align: center;
                margin: 1rem 0;
                position: relative;
            }
            .auth-divider:before {
                content: "";
                position: absolute;
                top: 50%;
                left: 0;
                right: 0;
                height: 1px;
                background: #e5e7eb;
            }
            .auth-divider span {
                background: white;
                padding: 0 0.5rem;
                color: #6b7280;
                position: relative;
                font-size: 0.875rem;
            }
            div[data-testid="stForm"] {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Center the form using columns
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        if st.session_state.get("show_register", False):
            st.markdown("""
                <div class="auth-header">
                    <div class="auth-title">Create Account</div>
                    <div class="auth-subtitle">Join our community of learners</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("register_form"):
                first_name = st.text_input("First Name", key="reg_first_name_modal", placeholder="Enter your first name")
                last_name = st.text_input("Last Name", key="reg_last_name_modal", placeholder="Enter your last name")
                email = st.text_input("Email", key="reg_email_modal", placeholder="Enter your email")
                password = st.text_input("Password", type="password", key="reg_password_modal", placeholder="Create a password")
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                if submitted:
                    success, msg = register(first_name, last_name, email, password)
                    if success:
                        st.success("Registration successful! Please log in.")
                        st.session_state["show_register"] = False
                        st.rerun()
                    else:
                        st.error(msg or "Registration failed. Email might already exist.")
            
            st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)
            if st.button("Back to Login", use_container_width=True):
                st.session_state["show_register"] = False
                st.rerun()
        else:
            st.markdown("""
                <div class="auth-header">
                    <div class="auth-title">Welcome Back</div>
                    <div class="auth-subtitle">Sign in to continue your learning journey</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email_modal", placeholder="Enter your email")
                password = st.text_input("Password", type="password", key="login_password_modal", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)
                if submitted:
                    success, result = login(email, password)
                    if success:
                        st.success("Login successful!")
                        st.session_state["show_login"] = False
                        st.session_state["is_authenticated"] = True
                        st.session_state["user_id"] = result
                        st.rerun()
                    else:
                        st.error(result or "Invalid email or password.")
            
            st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                st.session_state["show_register"] = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_auth_buttons():
    """Show login/register buttons in the sidebar"""
    with st.sidebar:
        if st.session_state['is_authenticated']:
            st.write(f"Welcome, {st.session_state['name']}!")
            if st.button("Logout"):
                logout()
                st.rerun()
        else:
            if st.button("Login"):
                st.session_state['show_login'] = True
                st.rerun()
            if st.button("Register"):
                st.session_state['show_register'] = True
                st.rerun()
