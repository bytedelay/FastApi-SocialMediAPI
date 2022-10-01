from ..import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import FastAPI, Response, status, HTTPException,APIRouter, Depends


router = APIRouter(prefix="/users",tags=['Users'])#This helps not mention the required path everytime
#app = FastAPI()

@router.post("/", status_code=status.HTTP_201_CREATED,response_model = schemas.RespondUser)
def cruser(user_check:schemas.UserCreate, db: Session = Depends(get_db)): 
    
    #hashing password for security
    crypt_pass = utils.hasher(user_check.password) #making a separate py for hashing 
    user_check.password = crypt_pass

    user_contents = models.Users(**user_check.dict())#unpacks dictionary #we are inserting so no query
    
    db.add(user_contents) #adds to database 
    db.commit() # commit operation in sql alchemy
    db.refresh(user_contents) #does the work of returning* in post gres
    return user_contents

#Fetching user by id

@router.get("/{id}",response_model = schemas.RespondUser)
def get_user(id:int, db: Session = Depends(get_db)):
    fetch_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not fetch_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    return fetch_user


@router.get("/",response_model = List[schemas.RespondUser]) #if not listed error occurs.
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users #stores the data in lists of dictionary
    #can see the results in postman
