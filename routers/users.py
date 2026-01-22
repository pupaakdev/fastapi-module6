import logging
from fastapi import APIRouter, HTTPException
from models.user import User, UserRequest, UserResponse, UserLoginRequest, UserLoginResponse
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from utils import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=UserResponse)
def create_user(user_req: UserRequest, db: Session = Depends(get_db)):
    logging.info("Register endpoint called.")

    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_req.username).first()
    if existing_user:
        raise HTTPException(status_code = 409, detail = f"Username {user_req.username} already taken.")
    
    # Check if email is already registered
    existing_email = db.query(User).filter(User.email == user_req.email).first()
    if existing_email:
        raise HTTPException(status_code = 409, detail = f"Email {user_req.email} is already registered.")
    
    # Create new user
    new_user = User(
        username = user_req.username,
        fullname = user_req.fullname,
        email = user_req.email,
        hashed_password = hash_password(user_req.password)
    )
    logging.info(f"Created user: {new_user}.")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    response = UserResponse(username = new_user.username, email = new_user.email)

    return response

@router.post("/login", response_model=UserLoginResponse)
def login_user(login_req: UserLoginRequest, db: Session = Depends(get_db)):
    logging.info("Login endpoint called.")
    
    # Find user by username
    user = db.query(User).filter(User.username == login_req.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    # Verify password
    if not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    logging.info(f"User {login_req.username} logged in successfully.")

    access_token = create_access_token(data={"sub": user.username})
    
    return UserLoginResponse(message="Login successful!", username=user.username, access_token = access_token)

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logging.info(f"Token received: {token}")
    try:
        logging.info("Decoding access token")
        payload = decode_access_token(token)
        logging.info(f"Payload decoded: {payload}")
        username: str = payload.get("sub")

        logging.info(f"Decoded username: {username}")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/", dependencies=[Depends(get_current_user)])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users

@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def delete_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.delete(user)
    db.commit()

    return "User deleted."