import psycopg2
from app.core.config import settings

def test_connection():
    try:
        # Parse the DATABASE_URL
        # Format: postgresql://user:password@localhost:5432/dbname
        conn = psycopg2.connect(settings.DATABASE_URL)
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Check for pgvector extension
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        vector_ext = cursor.fetchone()
        
        if vector_ext:
            print("pgvector extension is installed!")
        else:
            print("pgvector extension not installed")
            print("Installing it now...")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
            print("pgvector extension installed!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()