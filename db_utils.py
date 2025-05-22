import os
from datetime import datetime
import hashlib
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

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

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("\n" + "="*50)
        print("DATABASE CONNECTED SUCCESSFULLY!")
        print("="*50 + "\n")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def init_db():
    """Initialize the database with required tables"""
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
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
        finally:
            conn.close()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

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

def create_interview(user_id, category):
    """Create a new interview session"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO interviews (user_id, category)
                    VALUES (%s, %s)
                    RETURNING id
                ''', (user_id, category))
                
                interview_id = cur.fetchone()[0]
                conn.commit()
                return interview_id
        except Exception as e:
            print(f"Error creating interview: {str(e)}")
            return None
        finally:
            conn.close()
    return None

def save_question_response(interview_id, question, user_answer, model_answer, score, feedback, time_taken):
    """Save a question response"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO question_responses 
                    (interview_id, question, user_answer, model_answer, score, feedback, time_taken)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (interview_id, question, user_answer, model_answer, score, feedback, time_taken))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving question response: {str(e)}")
            return False
        finally:
            conn.close()
    return False

def update_interview_score(interview_id, score, total_questions):
    """Update interview score and completion status"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''
                    UPDATE interviews 
                    SET score = %s, total_questions = %s, completed_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (score, total_questions, interview_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating interview score: {str(e)}")
            return False
        finally:
            conn.close()
    return False

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