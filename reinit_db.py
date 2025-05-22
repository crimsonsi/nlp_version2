import psycopg2
from db_utils import DB_CONFIG

def reinit_db():
    """Reinitialize the database with the correct schema"""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            # Drop existing tables
            cur.execute("""
                DROP TABLE IF EXISTS question_responses CASCADE;
                DROP TABLE IF EXISTS interviews CASCADE;
                DROP TABLE IF EXISTS users CASCADE;
            """)
            
            # Create users table
            cur.execute('''
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create interviews table
            cur.execute('''
                CREATE TABLE interviews (
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
                CREATE TABLE question_responses (
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
            print("Database reinitialized successfully")
    except Exception as e:
        print(f"Error reinitializing database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    reinit_db() 