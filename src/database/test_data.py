from .config import SessionLocal
from .models import PostDB

def insert_sample_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(PostDB).first() is None:
            sample_posts = [
                PostDB(
                    title="First Post",
                    content="This is the content of my first post about FastAPI",
                    author="John Doe"
                ),
                PostDB(
                    title="Python Tips",
                    content="Here are some amazing Python tips and tricks...",
                    author="Jane Smith"
                ),
                PostDB(
                    title="SQLite with FastAPI",
                    content="Learn how to integrate SQLite with FastAPI...",
                    author="Bob Wilson"
                ),
                PostDB(
                    title="REST API Best Practices",
                    content="Essential REST API design principles and best practices...",
                    author="Alice Brown"
                )
            ]
            db.add_all(sample_posts)
            db.commit()
            print("Sample data inserted successfully!")
    except Exception as e:
        print(f"Error inserting sample data: {e}")
    finally:
        db.close() 