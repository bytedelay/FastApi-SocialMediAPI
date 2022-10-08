from ..import models,schemas,oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func 
from fastapi import Response, status, HTTPException,APIRouter,Depends
from typing import List, Optional


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']) 

@router.get("/", response_model = List[schemas.LikesDisplay])
def get_posts(db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user), limit :int = 10, skip: int = 0,
search: Optional[str] = ""):    
    results = db.query(models.Post,func.count(models.Likes.posts_id).label("no_of_likes")
    ).join(models.Likes,models.Likes.posts_id == models.Post.id,isouter = True).group_by(models.Post.id
    ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    return results 

@router.get('/{id}', response_model = schemas.LikesDisplay)
def get_post(id : int,db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user) ):
    fetched_post = db.query(models.Post,func.count(models.Likes.posts_id).label("no_of_likes")
    ).join(models.Likes,models.Likes.posts_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first() #using first cos using all() would search the entire db
    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    return fetched_post

 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Respond)
def crposts(post_check:schemas.POSTCreate, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)): #shifted the schema to schemas.py
    posted_contents = models.Post(owner_mailid = user_username.email,**post_check.dict())#unpacks dictionary #we are inserting so no query
    db.add(posted_contents) 
    db.commit()
    db.refresh(posted_contents)
    return posted_contents


@router.delete('/{id}', response_model = schemas.Respond)
def delete_post(id: int, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    integrity_check = deleted_post.first()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The ids:{id} provided is not present")
    if integrity_check.owner_mailid!=user_username.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized for this operation")
    deleted_post.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model = schemas.Respond)
def update_post(id: int, post:schemas.POSTCreate, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)): #ensuring id is type int and sending schema
    post_updated = db.query(models.Post).filter(models.Post.id == id)
    integrity_check = post_updated.first()
    if post_updated.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} provided is not present")
    if integrity_check.owner_mailid!=user_username.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized for this operation")
    post_updated.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_updated.first() 