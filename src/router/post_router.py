from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from src.models.post import Post, PostCreate, PostBase, PaginatedPosts
from src.database.config import get_db
from src.database.models import PostDB, User
from src.utils.logger import logger
from src.utils.auth import get_current_active_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"Creating new post with title: {post.title}")
    try:
        db_post = PostDB(**post.model_dump(), author_id=current_user.id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        logger.info(f"Successfully created post with ID: {db_post.id}")
        return db_post
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=PaginatedPosts)
async def get_all_posts(
    skip: int = Query(default=0, ge=0, description="Number of posts to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of posts to return"),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching posts with skip={skip} and limit={limit}")
    try:
        total = db.query(PostDB).count()
        posts = (
            db.query(PostDB)
            .order_by(PostDB.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        logger.info(f"Successfully retrieved {len(posts)} posts out of {total} total")
        return PaginatedPosts(
            items=posts,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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
async def update_post(
    post_id: int,
    post_update: PostBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"Updating post with ID: {post_id}")
    try:
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            logger.warning(f"Post with ID {post_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.author_id != current_user.id:
            logger.warning(f"User {current_user.username} attempted to update post {post_id} owned by user {post.author_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post"
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
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"Deleting post with ID: {post_id}")
    try:
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            logger.warning(f"Post with ID {post_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if post.author_id != current_user.id:
            logger.warning(f"User {current_user.username} attempted to delete post {post_id} owned by user {post.author_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
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