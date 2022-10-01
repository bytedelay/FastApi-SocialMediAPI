from ..import models,schemas,oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException,APIRouter,Depends
from typing import List, Optional

#router helps to declutter and make separate py's for each module
router = APIRouter(
    prefix = "/posts",
    tags=['Posts']) #This helps not mention the required path everytime
#app = FastAPI()


#fetching multiple posts now alchemy
@router.get("/", response_model = List[schemas.Respond])
def get_posts(db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user), limit :int = 10, skip: int = 0,
search: Optional[str] = ""): 
    #{{URL}}posts?limit=3 to use the feature
    #Limit adds limit to content default 10 unless user changes
    #posts = db.query(models.Post).filter(models.Post.owner_mailid == user_username)).all()   
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #limits the post
    #for searching content with spaces in between titles add %20.
    #Adding skip to skip particular posts
    #using offset to use skip feature.
    #helps in pagination
    return posts #stores the data in lists of dictionary




#fetching a single post
@router.get('/{id}', response_model = schemas.Respond)
def get_post(id : int,db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user) ):
    fetched_post = db.query(models.Post).filter(models.Post.id == id).first() #using first cos using all() would search the entire db
    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} is not found")
    return fetched_post


#Using to insert data into database 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Respond)
def crposts(post_check:schemas.POSTCreate, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)): #shifted the schema to schemas.py
    posted_contents = models.Post(owner_mailid = user_username.email,**post_check.dict())#unpacks dictionary #we are inserting so no query
    db.add(posted_contents) #adds to database 
    db.commit() # commit operation in sql alchemy
    db.refresh(posted_contents) #does the work of returning* in post gres
    #print(user_username.email)
    #print(posted_contents.owner_mailid)
    return posted_contents


#Deleting a post in database

@router.delete('/{id}', response_model = schemas.Respond)
def delete_post(id: int, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)):
#def delete_post(id: int, db: Session = Depends(get_db), user_username:int =Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    integrity_check = deleted_post.first()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The ids:{id} provided is not present")
    if integrity_check.owner_mailid!=user_username.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized for this operation")
    deleted_post.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model = schemas.Respond) #can also use patch as well
def update_post(id: int, post:schemas.POSTCreate, db: Session = Depends(get_db), user_username:str =Depends(oauth2.get_current_user)): #ensuring id is type int and sending schema
    post_updated = db.query(models.Post).filter(models.Post.id == id) #function returns index based on id
    integrity_check = post_updated.first()
    
    if post_updated.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} provided is not present")
    if integrity_check.owner_mailid!=user_username.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized for this operation")
    post_updated.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_updated.first() 