from fastapi import APIRouter, Depends, HTTPException
from models import User, Order
from dependencies import create_session, verify_token
from sqlalchemy.orm import Session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema, UserInfoSchema
from jose import jwt
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Helper functions:
def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + token_duration
    user_info = {"sub": str(user_id), "exp": expire_date}
    encoded_jwt = jwt.encode(user_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first() 
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

# Routes:
@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
        "access_token": access_token, 
        "token_access": "Bearer"
        }

@auth_router.get("/profile", response_model=UserInfoSchema)
async def get_user_info(user: User = Depends(verify_token), session: Session = Depends(create_session)):
    """
    Return the autenticated user's information, including their orders. 
    """
    orders = session.query(Order).filter(Order.user_id == user.id).all()

    orders_data = orders if orders else "No orders found for this user."

    user_info = UserInfoSchema(
        name=user.name,
        email=user.email,
        active=user.active,
        orders=orders_data
    )
    return user_info

@auth_router.post("/register", status_code=201)
async def create_user(user_schema: UserSchema, session: Session = Depends(create_session)): 
    user = session.query(User).filter(User.email == user_schema.email).first() 
    if user:
        raise HTTPException(status_code=400, detail="This email already exists.")
    else:
        hashed_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, hashed_password, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"message": f"User {user_schema.email} created successfully."}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(create_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session) 
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid user or password.")
    else: 
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {
            "access_token": access_token, # 30 minutes duration
            "refresh_token": refresh_token, # 7 days duration
            "token_access": "Bearer"
            }

@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(create_session)):
    """
    This route is for testing the login with form data, it works the same as the /login route but receives the data in a different way.
    """
    user = authenticate_user(form_data.username, form_data.password, session)  
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid user or password.")
    else: 
        access_token = create_token(user.id)
        return {
            "access_token": access_token, # 30 minutes duration
            "token_access": "Bearer"
            }
