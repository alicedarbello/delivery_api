from fastapi import Depends, HTTPException
from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from settings import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form") 

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
        sub = user_info.get("sub")
        if sub is None:
            raise JWTError("Invalid token: missing sub")
        user_id = int(sub)
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, verify the validity of your token.")
    user = session.query(User).filter(User.id ==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access denied.")
    return user