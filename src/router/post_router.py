from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from src.models.post import Post, PostCreate, PostBase
from src.database.config import get_db
from src.database.models import PostDB
from src.utils.logger import logger

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new post with title: {post.title}")
    try:
        db_post = PostDB(**post.model_dump())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        logger.info(f"Successfully created post with ID: {db_post.id}")
        return db_post
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Post])
async def get_all_posts(db: Session = Depends(get_db)):
    logger.info("Fetching all posts")
    try:
        posts = db.query(PostDB).all()
        logger.info(f"Successfully retrieved {len(posts)} posts")
        return posts
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching post with ID: {post_id}")
    try:
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            logger.warning(f"Post with ID {post_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        logger.info(f"Successfully retrieved post with ID: {post_id}")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostBase, db: Session = Depends(get_db)):
    logger.info(f"Updating post with ID: {post_id}")
    try:
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            logger.warning(f"Post with ID {post_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        for key, value in post_update.model_dump().items():
            setattr(post, key, value)
        
        db.commit()
        db.refresh(post)
        logger.info(f"Successfully updated post with ID: {post_id}")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting post with ID: {post_id}")
    try:
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            logger.warning(f"Post with ID {post_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        db.delete(post)
        db.commit()
        logger.info(f"Successfully deleted post with ID: {post_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")