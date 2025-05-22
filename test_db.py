from db_utils import get_db_connection, init_db
import psycopg2
from psycopg2.extras import DictCursor

def test_connection():
    """Test database connection and table creation"""
    print("Testing database connection...")
    
    # Test basic connection
    conn = get_db_connection()
    if conn:
        print("✅ Successfully connected to database")
        
        try:
            # Initialize database (create tables)
            init_db()
            print("✅ Database tables initialized")
            
            # Test if tables exist
            with conn.cursor(cursor_factory=DictCursor) as cur:
                # Check users table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    );
                """)
                if cur.fetchone()[0]:
                    print("✅ Users table exists")
                else:
                    print("❌ Users table not found")
                
                # Check interviews table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'interviews'
                    );
                """)
                if cur.fetchone()[0]:
                    print("✅ Interviews table exists")
                else:
                    print("❌ Interviews table not found")
                
                # Check question_responses table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'question_responses'
                    );
                """)
                if cur.fetchone()[0]:
                    print("✅ Question responses table exists")
                else:
                    print("❌ Question responses table not found")
                
                # Test inserting a test user
                try:
                    cur.execute("""
                        INSERT INTO users (name, email, password_hash)
                        VALUES (%s, %s, %s)
                        RETURNING id;
                    """, ('test_user', 'test@example.com', 'test_hash'))
                    user_id = cur.fetchone()[0]
                    print(f"✅ Successfully inserted test user (ID: {user_id})")
                    
                    # Test creating an interview
                    cur.execute("""
                        INSERT INTO interviews (user_id, category)
                        VALUES (%s, %s)
                        RETURNING id;
                    """, (user_id, 'test_category'))
                    interview_id = cur.fetchone()[0]
                    print(f"✅ Successfully created test interview (ID: {interview_id})")
                    
                    # Test inserting a question response
                    cur.execute("""
                        INSERT INTO question_responses 
                        (interview_id, question, user_answer, model_answer, score, feedback, time_taken)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING id;
                    """, (interview_id, 'Test question?', 'Test answer', 'Model answer', 8.5, 'Good answer!', 120))
                    response_id = cur.fetchone()[0]
                    print(f"✅ Successfully inserted test question response (ID: {response_id})")
                    
                    # Clean up test data
                    cur.execute("DELETE FROM question_responses WHERE interview_id = %s", (interview_id,))
                    cur.execute("DELETE FROM interviews WHERE id = %s", (interview_id,))
                    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    print("✅ Successfully cleaned up test data")
                    
                except psycopg2.Error as e:
                    print(f"❌ Error during test data operations: {str(e)}")
                
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error during database operations: {str(e)}")
        finally:
            conn.close()
            print("✅ Database connection closed")
    else:
        print("❌ Failed to connect to database")

if __name__ == "__main__":
    test_connection() 