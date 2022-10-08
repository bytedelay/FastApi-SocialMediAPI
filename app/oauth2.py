from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas,database,models
from .confg import settings

oath2_scheme  = OAuth2PasswordBearer(tokenUrl='login') 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def access_token_creation(data:dict):
    to_encode = data.copy() 

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        pr_username: str = decoded.get("username") #calling username 

        if pr_username is None:
            raise credentials_exception

        token_data = schemas.TokenData(email=pr_username)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oath2_scheme), db: Session =  Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.email == token.email).first()

    return user

