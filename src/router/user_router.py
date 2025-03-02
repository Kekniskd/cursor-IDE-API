from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database.config import get_db
from src.database.models import User
from src.models.user import UserCreate, User as UserSchema, UserUpdate
from src.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.utils.logger import logger

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register new user with username: {user.username}")
    
    # Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        logger.warning(f"Registration failed: Username {user.username} already exists")
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user.email).first():
        logger.warning(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Successfully registered user: {user.username}")
        return db_user
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error creating user"
        )

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for user: {form_data.username}")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    logger.info(f"User {current_user.username} accessed their profile")
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.username} attempting to update their profile")
    
    # Check if new username exists
    if user_update.username and user_update.username != current_user.username:
        if db.query(User).filter(User.username == user_update.username).first():
            logger.warning(f"Update failed: Username {user_update.username} already exists")
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
    
    # Check if new email exists
    if user_update.email and user_update.email != current_user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            logger.warning(f"Update failed: Email {user_update.email} already exists")
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
    
    # Update user fields
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    try:
        db.commit()
        db.refresh(current_user)
        logger.info(f"Successfully updated user profile for: {current_user.username}")
        return current_user
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error updating user"
        ) 