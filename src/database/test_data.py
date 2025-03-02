from .config import SessionLocal
from .models import PostDB, User
from src.utils.auth import get_password_hash
from src.utils.logger import logger

def insert_sample_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first() is None:
            # Create sample users
            sample_users = [
                User(
                    email="john@example.com",
                    username="johndoe",
                    hashed_password=get_password_hash("password123"),
                    is_active=True
                ),
                User(
                    email="jane@example.com",
                    username="janesmith",
                    hashed_password=get_password_hash("password456"),
                    is_active=True
                ),
                User(
                    email="bob@example.com",
                    username="bobwilson",
                    hashed_password=get_password_hash("password789"),
                    is_active=True
                )
            ]
            
            db.add_all(sample_users)
            db.commit()
            logger.info("Sample users created successfully!")

            # Create sample posts for each user
            john = db.query(User).filter(User.username == "johndoe").first()
            jane = db.query(User).filter(User.username == "janesmith").first()
            bob = db.query(User).filter(User.username == "bobwilson").first()

            sample_posts = [
                # John's posts
                PostDB(
                    title="Getting Started with FastAPI",
                    content="FastAPI is a modern Python web framework...",
                    author_id=john.id
                ),
                PostDB(
                    title="Python Best Practices",
                    content="Here are some Python coding best practices...",
                    author_id=john.id
                ),
                # Jane's posts
                PostDB(
                    title="SQLAlchemy Tips",
                    content="Essential SQLAlchemy tips and tricks...",
                    author_id=jane.id
                ),
                PostDB(
                    title="API Security",
                    content="Important security considerations for APIs...",
                    author_id=jane.id
                ),
                # Bob's posts
                PostDB(
                    title="Database Design",
                    content="Fundamentals of good database design...",
                    author_id=bob.id
                )
            ]
            
            db.add_all(sample_posts)
            db.commit()
            logger.info("Sample posts created successfully!")
            
    except Exception as e:
        logger.error(f"Error inserting sample data: {str(e)}")
        db.rollback()
    finally:
        db.close() 
        db.close() 