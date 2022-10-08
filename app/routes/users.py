from ..import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, HTTPException,APIRouter, Depends
from sqlalchemy import func


router = APIRouter(prefix="/users",tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model = schemas.RespondUser)
def cruser(user_check:schemas.UserCreate, db: Session = Depends(get_db)): 
    
    crypt_pass = utils.hasher(user_check.password) 
    user_check.password = crypt_pass
    user_contents = models.Users(**user_check.dict())
    db.add(user_contents) 
    db.commit()
    db.refresh(user_contents) 
    return user_contents

@router.get("/{id}")
def get_user(id:int, db: Session = Depends(get_db)):
    fetch_username = db.query(models.Users).filter(models.Users.id == id).first()
    fetch_user = db.query(models.Users.email,func.count(models.Follows.follower_mail).label("no_of_followers")
    ).join(models.Follows,models.Users.id == models.Follows.user_id,isouter = True
    ).group_by(models.Users.id).filter(models.Users.id == id).first()
    fetch_user_fol = db.query(models.Users.email,func.count(models.Follows.follower_mail).label("no_of_followings")
    ).join(models.Follows,models.Users.email == models.Follows.follower_mail,isouter = True
    ).group_by(models.Users.id).filter(models.Users.id == id).first()
    
    if not fetch_username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    if not fetch_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    if not fetch_user_fol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    
    return {"Results":f"username: {fetch_username.email.split('@')[0]}, No_of_Followers:{fetch_user.no_of_followers}, No_of _followings:{fetch_user_fol.no_of_followings}"}


@router.get("/",response_model = List[schemas.RespondUser])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users
