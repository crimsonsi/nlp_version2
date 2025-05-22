import streamlit as st
import hashlib
import secrets
import time
from db_utils import get_db_connection

def generate_session_token(user_id, name):
    """Generate a session token with expiration time"""
    token = secrets.token_hex(16)
    expiration = time.time() + (20 * 60)  # 20 minutes from now
    return token, expiration

def is_session_valid():
    """Check if the current session is valid"""
    if not all(key in st.session_state for key in ['session_token', 'session_expiration']):
        return False
    if st.session_state['session_token'] is None or st.session_state['session_expiration'] is None:
        return False
    return time.time() < float(st.session_state['session_expiration'])

def hash_password(password):
    """Hash a password using SHA-256"""
    salt = secrets.token_hex(8)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def verify_password(stored_password, provided_password):
    """Verify a password against its hash"""
    salt, hash_value = stored_password.split('$')
    hash_obj = hashlib.sha256((provided_password + salt).encode())
    return hash_obj.hexdigest() == hash_value

def register(first_name, last_name, email, password):
    """Register a new user in PostgreSQL"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Could not connect to database."
        with conn.cursor() as cur:
            # Check if email already exists
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cur.fetchone():
                conn.close()
                return False, "Email already exists"
            # Concatenate first_name and last_name into a single 'name' column
            name = f"{first_name} {last_name}"
            # Hash password and save user
            password_hash = hash_password(password)
            cur.execute('''
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (name, email, password_hash))
            conn.commit()
            conn.close()
            return True, "Registration successful"
    except Exception as e:
        return False, f"Error during registration: {str(e)}"

def login(email, password):
    """Login a user from PostgreSQL"""
    try:
        conn = get_db_connection()
        if not conn:
            return False, "Could not connect to database."
        with conn.cursor() as cur:
            cur.execute('SELECT id, password_hash, name FROM users WHERE email = %s', (email,))
            user = cur.fetchone()
            conn.close()
            if not user:
                return False, "User not found"
            user_id, stored_password, full_name = user
            if verify_password(stored_password, password):
                # Generate session token and set expiration
                token, expiration = generate_session_token(user_id, full_name)
                st.session_state['session_token'] = token
                st.session_state['session_expiration'] = expiration
                st.session_state['name'] = full_name
                return True, user_id
            else:
                return False, "Invalid password"
    except Exception as e:
        return False, f"Error during login: {str(e)}"

def logout():
    """Logout the current user"""
    st.session_state['is_authenticated'] = False
    st.session_state['name'] = None
    st.session_state['user_id'] = None
    st.session_state['session_token'] = None
    st.session_state['session_expiration'] = None

def init_auth_session():
    """Initialize authentication session state"""
    if 'is_authenticated' not in st.session_state:
        st.session_state['is_authenticated'] = False
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'session_token' not in st.session_state:
        st.session_state['session_token'] = None
    if 'session_expiration' not in st.session_state:
        st.session_state['session_expiration'] = None

    # Check if there's a valid session
    if is_session_valid():
        st.session_state['is_authenticated'] = True
    else:
        # Clear session if expired
        if 'session_token' in st.session_state:
            logout()
