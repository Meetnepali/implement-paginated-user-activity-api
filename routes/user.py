from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from typing import Dict
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "secret_key_123"  # In production, use a secure method to generate and store this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user storage: {email: {"email": ..., "password_hash": ..., "display_name": ...}}
user_db: Dict[str, Dict] = {}

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    display_name: constr(min_length=2, max_length=100)

class UserRegisterResponse(BaseModel):
    email: EmailStr
    display_name: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    detail: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserRegisterResponse, responses={
    400: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
})
def register_user(user: UserRegisterRequest):
    email = user.email.lower()
    if email in user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Store with hashed password
    user_db[email] = {
        "email": email,
        "password_hash": hash_password(user.password),
        "display_name": user.display_name
    }
    return UserRegisterResponse(email=email, display_name=user.display_name)

@router.post("/login", response_model=TokenResponse, responses={
    401: {"model": ErrorResponse},
    400: {"model": ErrorResponse}
})
def login_user(data: UserLoginRequest):
    email = data.email.lower()
    user = user_db.get(email)
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token_data = {"sub": email}
    token = create_access_token(token_data)
    return TokenResponse(access_token=token)
