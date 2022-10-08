
from ..import schemas,database,oauth2,models
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,APIRouter,Depends

router = APIRouter(prefix = '/like', tags=['Add Likes/Remove Likes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def likeness(vote:schemas.Like, db: Session = Depends(database.get_db), user_username:str=Depends(oauth2.get_current_user)):

    post_presence = db.query(models.Likes).filter(models.Post.id == vote.posts_id).first()

    if not post_presence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    like_check = db.query(models.Likes).filter(models.Likes.posts_id == vote.posts_id, 
        models.Likes.author_mail == user_username.email)
    liked = like_check.first()

    if (vote.dir==1):
        if liked:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"The current user {user_username.email.split('@')[0]} has already liked the post {vote.posts_id}")
            
        new_like = models.Likes(posts_id = vote.posts_id, author_mail = user_username.email)
        db.add(new_like)
        db.commit()

        return {"message":f"The Post {vote.posts_id} has been liked"}

    else:
        
        if not liked:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        like_check.delete(synchronize_session=False)
        db.commit()

        return {"message":f"You have withdrawn your like{user_username.email.split('@')[0]}"}
