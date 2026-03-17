from fastapi import Depends, HTTPException
from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

# Create a database session
def create_session():    
    try:     
        Session = sessionmaker(bind=db) 
        session = Session()
        yield session
    finally:
        session.close()

# Verify the token and get the current user
def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(create_session)): 
    try:
        user_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(user_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, verify the validity of your token.")
    user = session.query(User).filter(User.id ==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access denied.")
    return user