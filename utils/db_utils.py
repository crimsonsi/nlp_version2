import os
from datetime import datetime
import hashlib
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import streamlit as st
import asyncio

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

@st.cache_resource(ttl=3600)  # Cache for 1 hour
def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

def init_db():
    """Initialize the database with required tables"""
    if 'db_initialized' in st.session_state:
        return True
        
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Create users table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(64) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create interviews table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS interviews (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id),
                        category VARCHAR(50) NOT NULL,
                        score DECIMAL,
                        total_questions INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create question_responses table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS question_responses (
                        id SERIAL PRIMARY KEY,
                        interview_id INTEGER NOT NULL REFERENCES interviews(id),
                        question TEXT NOT NULL,
                        user_answer TEXT NOT NULL,
                        model_answer TEXT NOT NULL,
                        score DECIMAL NOT NULL,
                        feedback TEXT,
                        time_taken INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
            conn.commit()
            st.session_state['db_initialized'] = True
            return True
        except Exception as e:
            st.error(f"Error initializing database: {str(e)}")
            return False
        finally:
            conn.close()
    return False

def register_user(name, email, password):
    """Register a new user in the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        with conn.cursor() as cur:
            # Check if email already exists
            cur.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cur.fetchone():
                conn.close()
                return None
            
            # Hash password and save user
            password_hash = hash_password(password)
            cur.execute('''
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (name, email, password_hash))
            user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return user_id
    except Exception as e:
        print(f"Error registering user: {str(e)}")
        return None

def verify_user(email, password):
    """Verify user credentials and return user info if valid"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        with conn.cursor() as cur:
            password_hash = hash_password(password)
            cur.execute('''
                SELECT id, name FROM users
                WHERE email = %s AND password_hash = %s
            ''', (email, password_hash))
            user = cur.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1]
                }
            return None
    except Exception as e:
        print(f"Error verifying user: {str(e)}")
        return None

def save_interview_results(user_id, category, score, feedback):
    """Save interview results to the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO interviews (user_id, category, score, feedback)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            ''', (user_id, category, score, feedback))
            interview_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error saving interview results: {str(e)}")
        return False

def get_user_history(user_id):
    """Get interview history for a user"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                SELECT category, score, feedback, completed_at
                FROM interviews
                WHERE user_id = %s
                ORDER BY completed_at DESC
            ''', (user_id,))
            history = cur.fetchall()
            conn.close()
            return [dict(h) for h in history]
    except Exception as e:
        print(f"Error getting user history: {str(e)}")
        return []

def get_user_stats(user_id):
    """Get statistics for a user"""
    try:
        conn = get_db_connection()
        if not conn:
            return {
                'total_interviews': 0,
                'average_score': 0,
                'best_score': 0,
                'worst_score': 0
            }
        
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    COUNT(*) as total_interviews,
                    AVG(score) as average_score,
                    MAX(score) as best_score,
                    MIN(score) as worst_score
                FROM interviews
                WHERE user_id = %s
            ''', (user_id,))
            stats = cur.fetchone()
            conn.close()
            
            return {
                'total_interviews': stats[0],
                'average_score': stats[1],
                'best_score': stats[2],
                'worst_score': stats[3]
            }
    except Exception as e:
        print(f"Error getting user stats: {str(e)}")
        return {
            'total_interviews': 0,
            'average_score': 0,
            'best_score': 0,
            'worst_score': 0
        }

def get_user_interviews(user_id):
    """Get all interviews for a user"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT id, category, score, total_questions, completed_at
                    FROM interviews
                    WHERE user_id = %s
                    ORDER BY completed_at DESC
                ''', (user_id,))
                
                interviews = cur.fetchall()
                return [dict(i) for i in interviews]
        except Exception as e:
            print(f"Error getting user interviews: {str(e)}")
            return []
        finally:
            conn.close()
    return []

def get_interview_responses(interview_id):
    """Get all responses for an interview"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT question, user_answer, model_answer, score, feedback, time_taken
                    FROM question_responses
                    WHERE interview_id = %s
                    ORDER BY created_at ASC
                ''', (interview_id,))
                
                responses = cur.fetchall()
                return [dict(r) for r in responses]
        except Exception as e:
            print(f"Error getting interview responses: {str(e)}")
            return []
        finally:
            conn.close()
    return []
